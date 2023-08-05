from collections import defaultdict
from GenRS.Alg.alg import Alg
import tensorflow as tf
import random
import numpy as np
import logging
import time


class Cfgan(Alg):

    def __init__(self, data, alg_cfg):
        """
        :param data: DataManager instance
        :param alg_cfg: dictionary that contains all options for the specific cfgan algorithm in the form [key]: value
        """
        super().__init__(data)
        tf.compat.v1.disable_eager_execution()
        self.alg_cfg = alg_cfg
        self.g_loss = 0
        self.d_loss = 0
        self.test_us = self.data.test_te_us

        self.ratings = []

    def execute_training(self):
        us_count_backup = self.data.n_us
        it_count_backup = self.data.n_it

        tr_set = self.data.whole_tr_dict  # tr[us] = list of items rated by us

        batch_count = it_count_backup
        us_count = us_count_backup
        train_dict = defaultdict(lambda: [0] * us_count)

        for us, i_list in tr_set.items():
            for it in i_list:
                train_dict[it][us] = 1

        tr_vec = []
        for batch_id in range(batch_count):
            tr_vec.append(train_dict[batch_id])

        tr_vec = np.array(tr_vec)

        mask_vec = tr_vec

        # prepare for the random negative sampling (memory inefficient)
        unobs = []
        for batch_id in range(batch_count):
            unobs.append(list(np.where(tr_vec[batch_id] == 0)[0]))  # list of [0] where the condition is true

        batch_list = np.arange(batch_count)

        # From here on the operations will be added to the graph instead of being executed eagerly
        with tf.Graph().as_default():
            # G
            # note that we don't use the random noise z
            condition = tf.compat.v1.placeholder(tf.float32, [None, us_count])
            G_output, G_L2norm, G_ZR_loss, G_ZR_dims = GEN(condition, us_count, self.alg_cfg['hidden_dim_g'],
                                                           self.alg_cfg['activation_function'],
                                                           self.alg_cfg['hidden_layer_g'])
            # D
            mask = tf.compat.v1.placeholder(tf.float32, [None, us_count])  # purchased = 1, otherwise 0
            fake_data = G_output * mask
            fake_data = tf.concat([condition, fake_data], 1)  # concatenate the two arrays through axis=1

            real_data = tf.compat.v1.placeholder(tf.float32, [None, us_count])
            _real_data = tf.concat([condition, real_data],
                                   1)  # concatenate them to obtain a placeholder with shape = (?, userCount*2)

            # create discriminators of real and fake data
            D_real = DIS(_real_data, us_count * 2, self.alg_cfg['hidden_dim_g'], self.alg_cfg['activation_function'],
                         self.alg_cfg['hidden_dim_d'])
            D_fake = DIS(fake_data, us_count * 2, self.alg_cfg['hidden_dim_g'], self.alg_cfg['activation_function'],
                         self.alg_cfg['hidden_dim_d'], _reuse=True)

            g_vars = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES,
                                                 scope='gen')  # the subset of Variable objects that will be trained by an optimizer in the variable_scope='gen' returns WEIGHTS, BIASES, ACTIVATION
            d_vars = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES,
                                                 scope='dis')  # the subset of Variable objects that will be trained by an optimizer in the variable_scope='dis' returns WEIGHTS, BIASES, ACTIVATION

            # define loss & optimizer for G
            g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_fake, labels=tf.ones_like(
                D_fake)))  # Computes the sigmoid cross entropy given logits and return the mean of the componentwise logistic losses.
            g_loss = g_loss + self.alg_cfg[
                'reg_g'] * G_L2norm  # normalize values of g_loss through the reg_G parameter multiplied to the L2norm of G
            if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'ZR':
                g_loss = g_loss + self.alg_cfg['ZR_coefficient'] * G_ZR_loss

            if self.alg_cfg['opt_g'] == 'sgd':  # optimizer = stochastic gradient descent with minimization loss
                trainer_G = tf.train.GradientDescentOptimizer(self.alg_cfg['lr_g']).minimize(g_loss, var_list=g_vars)
            elif self.alg_cfg['opt_g'] == 'adam':  # optimizer = adam optimizer with minimization loss
                trainer_G = tf.compat.v1.train.AdamOptimizer(self.alg_cfg['lr_g']).minimize(g_loss, var_list=g_vars)

            # define loss & optimizer for D
            d_loss_real = tf.reduce_mean(
                tf.nn.sigmoid_cross_entropy_with_logits(logits=D_real, labels=tf.ones_like(D_real)))
            d_loss_fake = tf.reduce_mean(
                tf.nn.sigmoid_cross_entropy_with_logits(logits=D_fake, labels=tf.zeros_like(D_fake)))

            D_L2norm = 0
            for pr in d_vars:  # for each parameter in the discriminator
                D_L2norm = D_L2norm + tf.nn.l2_loss(pr)
            d_loss = d_loss_real + d_loss_fake + self.alg_cfg['reg_d'] * D_L2norm

            if self.alg_cfg['opt_d'] == 'sgd':
                trainer_D = tf.train.GradientDescentOptimizer(self.alg_cfg['lr_d']).minimize(d_loss, var_list=d_vars)
            elif self.alg_cfg['opt_d'] == 'adam':
                trainer_D = tf.compat.v1.train.AdamOptimizer(self.alg_cfg['lr_d']).minimize(d_loss, var_list=d_vars)

            if self.alg_cfg['use_gpu']:
                config = tf.compat.v1.ConfigProto()  # or tf.compat.v1.ConfigProto
                config.gpu_options.allow_growth = True

            else:
                config = tf.compat.v1.ConfigProto(device_count={'GPU': 0})

            sess = tf.compat.v1.Session(config=config)
            init_op = tf.compat.v1.variables_initializer(tf.compat.v1.global_variables())
            sess.run(init_op)  # add all the variables to the graph
            saver = tf.train.Saver()

            tot_epochs = self.alg_cfg['n_epochs']
            tot_epochs = int(tot_epochs / self.alg_cfg['step_g'])

            for epoch in range(tot_epochs):
                # first perform the negative sampling for PM and ZR for this epoch
                n_samples_ZR = []
                n_samples_PM = []

                for batch_id in range(
                        batch_count):  # for user_id if mode=="userBased" else item_id if mode=="itemBased"
                    # ZR
                    if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'ZR':
                        # seed = int(time.time())     # TODO check about this information: original was seed= int(time.time())
                        np.random.seed(
                            self.data.data.settings.seed)  # Check it: before the changes was np.random.seed(seed)
                        n_samples_ZR.append(
                            np.random.choice(unobs[batch_id],
                                             int(len(unobs[batch_id]) * self.alg_cfg['ZR_ratio'] / 100),
                                             replace=False))

                    # PM
                    if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'PM':
                        # seed = int(time.time())   # TODO check about this information: original was seed= int(time.time())
                        np.random.seed(
                            self.data.data.settings.seed)  # Check it: before the changes was np.random.seed(seed)
                        n_samples_PM.append(
                            np.random.choice(unobs[batch_id],
                                             int(len(unobs[batch_id]) * self.alg_cfg['ZP_ratio'] / 100),
                                             replace=False))

                # D step
                num_of_minibatches = int(len(batch_list) / self.alg_cfg['batch_size_d']) + 1
                num_of_last_minibatch = len(batch_list) % self.alg_cfg['batch_size_d']

                for epoch_D in range(self.alg_cfg['step_d']):
                    # t1 = time.time()  # number of seconds elapsed since January 1 1970
                    loss_d = 0

                    random.seed(self.data.data.settings.seed)
                    random.shuffle(batch_list)

                    for batch_id in range(num_of_minibatches):
                        start = batch_id * self.alg_cfg['batch_size_d']
                        if batch_id == num_of_minibatches - 1:  # if it is the last minibatch
                            num_of_batches = num_of_last_minibatch
                        else:
                            num_of_batches = self.alg_cfg['batch_size_d']
                        end = start + num_of_batches
                        batch_index = batch_list[start: end]

                        trainMask = []
                        for batch_id in batch_index:
                            # PM, convert 0 to 1 in the masking vector e_u
                            if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'PM':
                                tmp = np.copy(mask_vec[batch_id])
                                tmp[n_samples_PM[batch_id]] = 1
                                trainMask.append(tmp)
                            else:
                                trainMask.append(mask_vec[batch_id])

                        _, dLoss = sess.run([trainer_D, d_loss],
                                            feed_dict={real_data: tr_vec[batch_index], mask: trainMask,
                                                       condition: tr_vec[batch_index]})  # Update D

                        loss_d = loss_d + dLoss
                        self.d_loss = loss_d

                    # t2 = time.time()  # number of seconds elapsed since January 1 1970
                    logging.log(level=logging.DEBUG,
                                msg="[{:d}: D][{:d}] cost:{:4f}, within {:s} seconds".format(epoch + 1, epoch_D + 1,
                                                                                             loss_d, str(t2 - t1)))

                # G step
                num_of_minibatches = int(len(batch_list) / self.alg_cfg['batch_size_g']) + 1
                num_of_last_minibatch = len(batch_list) % self.alg_cfg['batch_size_g']
                for epoch_G in range(self.alg_cfg['step_g']):
                    # t1 = time.time()  # number of seconds elapsed since January 1 1970
                    loss_g = 0

                    # random.seed(seed)         # Todo: check the changes: this line was the default one
                    random.seed(self.data.data.settings.seed)  # this is the new one
                    random.shuffle(batch_list)

                    for batch_id in range(num_of_minibatches):
                        start = batch_id * self.alg_cfg['batch_size_g']
                        if batch_id == num_of_minibatches - 1:  # if it is the last minibatch
                            num_of_batches = num_of_last_minibatch
                        else:
                            num_of_batches = self.alg_cfg['batch_size_g']
                        end = start + num_of_batches
                        batch_index = batch_list[start: end]

                        trainMask = []
                        trainZRMask = []

                        for batch_id in batch_index:
                            # PM, convert 0 to 1 in the masking vector e_u
                            if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'PM':
                                tmp = np.copy(mask_vec[batch_id])
                                tmp[n_samples_PM[batch_id]] = 1
                                trainMask.append(tmp)
                            else:
                                trainMask.append(mask_vec[batch_id])

                            # ZR
                            tmp = np.zeros(us_count)
                            if self.alg_cfg['scheme'] == 'ZP' or self.alg_cfg['scheme'] == 'ZR':
                                tmp[n_samples_ZR[batch_id]] = 1
                                trainZRMask.append(tmp)
                            else:
                                trainZRMask.append(tmp)

                        _, gLoss = sess.run([trainer_G, g_loss],
                                            feed_dict={condition: tr_vec[batch_index], mask: trainMask,
                                                       real_data: tr_vec[batch_index],
                                                       G_ZR_dims: trainZRMask})  # Update G

                        loss_g = loss_g + gLoss
                        self.g_loss = loss_g

                    logging.log(level=logging.DEBUG,
                                msg="[{:d}: G][{:d}] cost:{:4f}, within {:s} seconds".format(epoch + 1, epoch_G + 1,
                                                                                             loss_g, str(t2 - t1)))

                    # measure accuracy
                    # t1 = time.time()
                    all_ratings = sess.run(G_output, feed_dict={condition: tr_vec})
                    if self.alg_cfg['mode'] == "item_based":
                        all_ratings = np.transpose(all_ratings)

            self.save_training(saver, sess)
            # self.session.close()

        self.ratings = all_ratings
        return all_ratings

    def prediction(self, all_ratings):
        tr_matr = self.data.whole_tr_matr[self.data.test_te_us]
        all_ratings[tr_matr.nonzero()] = -np.inf
        return all_ratings


def FullyConnectedLayer(input, inputDim, outputDim, activation, model, layer, reuse=False):
    """
    :param input: placeholder with the choosen shape
    :param inputDim: shape of the input
    :param outputDim:
    :param activation: activation function (sigmoid)
    :param model: dis or gen
    :param layer: number of layer that is building
    :param reuse: if true the model reuse the same variables previously declared in tf.Graph
    :return y, L2norm, W, b: the output vector, the sum of the L2norm of Weights and bias, the Weights and the bias
    """
    scale1 = np.sqrt(6 / (inputDim + outputDim))

    wName = model + "_W" + str(layer)
    bName = model + "_B" + str(layer)

    with tf.compat.v1.variable_scope(model) as scope:

        if reuse == True:
            scope.reuse_variables()

        W = tf.compat.v1.get_variable(wName, [inputDim, outputDim],
                                      initializer=tf.random_uniform_initializer(-scale1, scale1))
        b = tf.compat.v1.get_variable(bName, [outputDim], initializer=tf.random_uniform_initializer(-0.01, 0.01))

        y = tf.matmul(input, W) + b

        L2norm = tf.nn.l2_loss(W) + tf.nn.l2_loss(b)

        if activation == "none":
            y = tf.identity(y, name="output")
            return y, L2norm, W, b

        elif activation == "sigmoid":
            return tf.nn.sigmoid(y), L2norm, W, b

        elif activation == "tanh":
            return tf.nn.tanh(y), L2norm, W, b


def GEN(input, userCount, h, activation, hiddenLayers):
    """
    :param input: placeholder with shape=(None, userCount)
    :param userCount: dimension
    :param h: dimension of the hidden layers
    :param activation: activation function of Generative model
    :param hiddenLayers: number of the hidden layers
    :return y, L2norm, ZR_loss, ZR_dims: output tensor, L2norm as the sum of L2norms computed, loss_function of ZR, ZR_dims tensor
    """
    ZR_dims = tf.compat.v1.placeholder(tf.float32, [None, userCount])

    # input->hidden
    y, L2norm, W, b = FullyConnectedLayer(input, userCount, h, activation, "gen", 0)

    # stacked hidden layers
    for layer in range(hiddenLayers - 1):
        y, this_L2, W, b = FullyConnectedLayer(y, h, h, activation, "gen", layer + 1)
        L2norm = L2norm + this_L2

    # hidden -> output
    y, this_L2, W, b = FullyConnectedLayer(y, h, userCount, "none", "gen", hiddenLayers + 1)
    L2norm = L2norm + this_L2

    # loss function for ZR
    ZR_loss = tf.reduce_mean(tf.reduce_sum(tf.square(y - 0) * ZR_dims, 1, keepdims=True))

    return y, L2norm, ZR_loss, ZR_dims,


def DIS(input, inputDim, h, activation, hiddenLayers, _reuse=False):
    # input->hidden
    y, _, W, b = FullyConnectedLayer(input, inputDim, h, activation, "dis", 0, reuse=_reuse)

    # stacked hidden layers
    for layer in range(hiddenLayers - 1):
        y, _, W, b = FullyConnectedLayer(y, h, h, activation, "dis", layer + 1, reuse=_reuse)

    # hidden -> output
    y, _, W, b = FullyConnectedLayer(y, h, 1, "none", "dis", hiddenLayers + 1, reuse=_reuse)

    return y
