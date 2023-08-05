from collections import defaultdict

from GenRS.Alg.alg import Alg
import tensorflow as tf
import random
import numpy as np
import logging
import time



class GEN:
    def __init__(self, itemNum, userNum, emb_dim, lamda, param=None, initdelta=0.05, learning_rate=0.05):
        self.itemNum = itemNum
        self.userNum = userNum
        self.emb_dim = emb_dim
        self.lamda = lamda  # regularization parameters
        self.param = param
        self.initdelta = initdelta
        self.learning_rate = learning_rate
        self.g_params = []

        with tf.compat.v1.variable_scope('generator'):
            if self.param is None:
                self.user_embeddings = tf.Variable(         # create a matrix in the form n_us x emb_dim with values in range (-initdelta, initdelta)
                    tf.random_uniform([self.userNum, self.emb_dim], minval=-self.initdelta, maxval=self.initdelta,
                                      dtype=tf.float32))
                self.item_embeddings = tf.Variable(         # create a matrix in the form n_it x emb_dim with values in range (-initdelta, initdelta)
                    tf.random_uniform([self.itemNum, self.emb_dim], minval=-self.initdelta, maxval=self.initdelta,
                                      dtype=tf.float32))
                self.item_bias = tf.Variable(tf.zeros([self.itemNum]))      # create an array of n_it zeros used for item_bias (mean of ratings?)

            else:       # if a model is already built
                self.user_embeddings = tf.Variable(self.param[0])       # load user_emb
                self.item_embeddings = tf.Variable(self.param[1])       # load item_emb
                self.item_bias = tf.Variable(param[2])      # load item_bias

            self.g_params = [self.user_embeddings, self.item_embeddings, self.item_bias]    # build array with g_params

        self.u = tf.compat.v1.placeholder(tf.int32)     # user
        self.i = tf.compat.v1.placeholder(tf.int32)     # item
        self.reward = tf.compat.v1.placeholder(tf.float32)      # reward

        self.u_embedding = tf.nn.embedding_lookup(self.user_embeddings, self.u)     # split embedding tensor by u_value
        self.i_embedding = tf.nn.embedding_lookup(self.item_embeddings, self.i)     # split embedding tensor by i_value
        self.i_bias = tf.gather(self.item_bias, self.i)         # split item_bias through index i

        self.all_logits = tf.reduce_sum(tf.multiply(self.u_embedding, self.item_embeddings), 1) + self.item_bias        # sum of each element in the columns of matrix u_emb x i_emb and add it_bias values to it
        self.i_prob = tf.gather(        # probability that i is taken by the split
            tf.reshape(tf.nn.softmax(tf.reshape(self.all_logits, [1, -1])), [-1]),
            self.i)     # softmax = tf.exp(logits) / tf.reduce_sum(tf.exp(logits), axis)

        # COMMENT: loss_gan = - media( log(i_prob) * reward) + lambda * sum(u_emb**2)/2 + sum(i_emb **2)/2 + sum(i_bias**2)/2
        self.gan_loss = -tf.reduce_mean(tf.compat.v1.log(self.i_prob) * self.reward) + self.lamda * (
            tf.nn.l2_loss(self.u_embedding) + tf.nn.l2_loss(self.i_embedding) + tf.nn.l2_loss(self.i_bias))

        g_opt = tf.compat.v1.train.GradientDescentOptimizer(self.learning_rate)     # create an instance of gr_descent optimizer with lr
        self.gan_updates = g_opt.minimize(self.gan_loss, var_list=self.g_params)        # compute gr_desc upon the g_params in order to minimize loss

        # for test stage, self.u: [batch_size]
        self.all_rating = tf.matmul(self.u_embedding, self.item_embeddings, transpose_a=False,
                                    transpose_b=True) + self.item_bias

class DIS:
    def __init__(self, itemNum, userNum, emb_dim, lamda, param=None, initdelta=0.05, learning_rate=0.05):
        self.itemNum = itemNum
        self.userNum = userNum
        self.emb_dim = emb_dim
        self.lamda = lamda  # regularization parameters
        self.param = param
        self.initdelta = initdelta
        self.learning_rate = learning_rate
        self.d_params = []

        with tf.compat.v1.variable_scope('discriminator'):
            if self.param is None:
                self.user_embeddings = tf.Variable(
                    tf.compat.v1.random_uniform([self.userNum, self.emb_dim], minval=-self.initdelta, maxval=self.initdelta,
                                      dtype=tf.float32))
                self.item_embeddings = tf.Variable(
                    tf.compat.v1.random_uniform([self.itemNum, self.emb_dim], minval=-self.initdelta, maxval=self.initdelta,
                                      dtype=tf.float32))
                self.item_bias = tf.compat.v1.Variable(tf.zeros([self.itemNum]))
            else:
                self.user_embeddings = tf.compat.v1.Variable(self.param[0])
                self.item_embeddings = tf.compat.v1.Variable(self.param[1])
                self.item_bias = tf.compat.v1.Variable(self.param[2])

        self.d_params = [self.user_embeddings, self.item_embeddings, self.item_bias]

        # placeholder definition
        self.u = tf.compat.v1.placeholder(tf.int32)
        self.i = tf.compat.v1.placeholder(tf.int32)
        self.label = tf.compat.v1.placeholder(tf.float32)

        self.u_embedding = tf.nn.embedding_lookup(self.user_embeddings, self.u)
        self.i_embedding = tf.nn.embedding_lookup(self.item_embeddings, self.i)
        self.i_bias = tf.gather(self.item_bias, self.i)

        # sum of each elements in matrix u_emb x i_emb through columns and add i_bias to the results
        self.pre_logits = tf.reduce_sum(tf.multiply(self.u_embedding, self.i_embedding), 1) + self.i_bias
        # x=logits, z=labels
        # pre_loss = x - x * z + log(1 + exp(-x)) + lambda * sum(u_emb **2)/2 + sum(i_emb ** 2)/2 + sum(i_bias **2)/2
        self.pre_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=self.label,
                                                                logits=self.pre_logits) + self.lamda * (
            tf.nn.l2_loss(self.u_embedding) + tf.nn.l2_loss(self.i_embedding) + tf.nn.l2_loss(self.i_bias)
        )


        d_opt = tf.compat.v1.train.GradientDescentOptimizer(self.learning_rate)     # create d_optimizer
        self.d_updates = d_opt.minimize(self.pre_loss, var_list=self.d_params)      # optimize d with pre_loss changing d_par

        # sum( u_emb x i_emb through columns) + i_bias
        self.reward_logits = tf.reduce_sum(tf.multiply(self.u_embedding, self.i_embedding),
                                           1) + self.i_bias
        # final reward is 2 * ( 1 / (1 + exp(-rew_log) ) - 0.5)
        self.reward = 2 * (tf.sigmoid(self.reward_logits) - 0.5)

        # for test stage, self.u: [batch_size]
        self.all_rating = tf.matmul(self.u_embedding, self.item_embeddings, transpose_a=False,
                                    transpose_b=True) + self.item_bias      # all_r = u_emb * transpose(i_emb)

        # sum each elements of matrix through columns (u_emb x i_emb) + it_bias
        self.all_logits = tf.reduce_sum(tf.multiply(self.u_embedding, self.item_embeddings), 1) + self.item_bias

        # NLL stands for negative-log-likelihood and represent a loss function that we have to minimize
        # - mean(log(y))
        self.NLL = -tf.reduce_mean(tf.compat.v1.log(
            tf.gather(tf.reshape(tf.nn.softmax(tf.reshape(self.all_logits, [1, -1])), [-1]), self.i))
        )
        # for dns sample
        self.dns_rating = tf.reduce_sum(tf.multiply(self.u_embedding, self.item_embeddings), 1) + self.item_bias


class Irgan(Alg):

    def __init__(self, data, alg_cfg):
        """
        :param data: DataManager instance
        :param alg_cfg: dictionary that contains all options for the specific cfgan algorithm in the form [key]: value
        """
        super().__init__(data)
        self.alg_cfg = alg_cfg
        tf.compat.v1.disable_eager_execution()

    # Get batch data from training set
    @staticmethod
    def get_batch_data(data, index, size):  # 1,5->1,2,3,4,5
        user = []
        item = []
        label = []
        for i in range(index, index + size):
            line = data[i]
            line = line.strip()
            line = line.split()
            user.append(int(line[0]))
            user.append(int(line[0]))
            item.append(int(line[1]))
            item.append(int(line[2]))
            label.append(1.)
            label.append(0.)
        return user, item, label

    def execute_training(self):
        generator = GEN(self.data.n_it, self.data.n_us, self.alg_cfg['latent_factor'], lamda=self.alg_cfg['lambda_gen'] / self.alg_cfg['batch_size'], param=self.alg_cfg['params_g'], initdelta=self.alg_cfg['init_delta'],
                        learning_rate=self.alg_cfg['lr_g'])
        discriminator = DIS(self.data.n_it, self.data.n_us, self.alg_cfg['latent_factor'], lamda=self.alg_cfg['lambda_dis'] / self.alg_cfg['batch_size'], param=self.alg_cfg['params_d'], initdelta=self.alg_cfg['init_delta'],
                            learning_rate=self.alg_cfg['lr_d'])

        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.compat.v1.Session(config=config)
        sess.run(tf.compat.v1.global_variables_initializer())

        dis_log = open('./dis_log.txt', 'w')
        gen_log = open('./gen_log.txt', 'w')

        # TODO Understand if remove the comment or not
        # predicted_ = []

        # minimax training
        best = 0.
        tr_data = []
        for epoch in range(self.alg_cfg['n_epochs']):
            for d_epoch in range(self.alg_cfg['n_epochs_d']):
                if d_epoch % 5 == 0:
                    tr_data = self.generate_for_d(sess, generator,
                                       self.alg_cfg['dis_tr_path'])  # write file with data generated by the generator
                    tr_size = len(tr_data)  # return the length of the file just filled
                index = 1     # =1 if index of line in file
                # index = 0
                while True:
                    if index > tr_size:
                        break
                    if index + self.alg_cfg['batch_size'] <= tr_size + 1:  # if there are other data in file to get
                        input_user, input_item, input_label = self.get_batch_data(tr_data, index, self.alg_cfg['batch_size'])
                    else:
                        input_user, input_item, input_label = self.get_batch_data(tr_data, index,
                                                                                  tr_size - index)  # take the first element
                    index += self.alg_cfg['batch_size']  # increment the index to the new starting point for batch_size data

                    _ = sess.run(discriminator.d_updates,
                                 feed_dict={discriminator.u: input_user, discriminator.i: input_item,
                                            discriminator.label: input_label})  # run the optimization

            # Train G
            for g_epoch in range(self.alg_cfg['n_epochs_g']):  # 50
                for u in self.data.whole_tr_dict:  # for each user in training set
                    sample_lambda = self.alg_cfg['temp_factor']  # temperature parameter value
                    pos = self.data.whole_tr_dict[u]  # get list of items at user pos

                    rating = sess.run(generator.all_logits,
                                      {generator.u: u})  # get the ratings returned by the generator
                    exp_rating = np.exp(rating)
                    prob = exp_rating / np.sum(exp_rating)  # prob is generator distribution p_\theta

                    pn = (1 - sample_lambda) * prob
                    pn[pos] += sample_lambda * 1.0 / len(pos)
                    # Now, pn is the Pn in importance sampling, prob is generator distribution p_\theta

                    sample = np.random.choice(np.arange(self.data.n_it), 2 * len(pos), p=pn)
                    ###########################################################################
                    # Get reward and adapt it with importance sampling
                    ###########################################################################
                    reward = sess.run(discriminator.reward, {discriminator.u: u, discriminator.i: sample})
                    reward = reward * prob[sample] / pn[sample]
                    ###########################################################################
                    # Update G
                    ###########################################################################
                    _ = sess.run(generator.gan_updates,
                                 {generator.u: u, generator.i: sample, generator.reward: reward})

            predicted_ = sess.run(generator.all_rating, {generator.u: self.data.test_te_us})
            # pr_val = {u: predicted_[i] for i, u in enumerate(self.data.test_te_us)}
            # generator.save_model(sess, "irgan_generator.pkl")
        gen_log.close()
        dis_log.close()
        return predicted_

    def prediction(self, all_ratings):
        tr_matr = self.data.whole_tr_matr[self.data.test_te_us]
        all_ratings[tr_matr.nonzero()] = -np.inf
        return all_ratings

    def generate_for_d(self, sess, model, filename):
        data = []
        for u in self.data.whole_tr_dict:  # for each user in training set
            pos = self.data.whole_tr_dict[u]  # pos = [list of items indices]

            rating = sess.run(model.all_rating, {model.u: [u]})  # extract the rating results created by the model
            rating = np.array(rating[0]) / self.alg_cfg['temp_factor']  # Temperature factor
            exp_rating = np.exp(rating)  # e^(rating)
            prob = exp_rating / np.sum(exp_rating)  # e^rating / sum(e^rating)

            neg = np.random.choice(np.arange(self.data.n_it), size=len(pos),
                                   p=prob)  # extract len(pos) items, each one with probability=prob
            for i in range(len(pos)):
                data.append(str(u) + '\t' + str(pos[i]) + '\t' + str(neg[i]))  # add the string to data

        with open(filename, 'w')as fout:
            fout.write('\n'.join(
                data))  # write each values in filename file followed by a \n, useful way to print a set of strings to file
        return data




