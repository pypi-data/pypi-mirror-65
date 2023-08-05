import os
import shutil

from scipy import sparse
from GenRS.Alg.alg import Alg
import numpy as np
import bottleneck as bn
import tensorflow as tf
from tensorflow_core.contrib.layers.python.layers.regularizers import l2_regularizer, apply_regularization


class Dae(Alg):
    def __init__(self, data, alg_cfg):
        super().__init__(data)
        tf.reset_default_graph()
        self.alg_cfg = alg_cfg
        self.p_dims = [self.alg_cfg['input_p'], self.data.n_it]
        self.q_dims = self.p_dims[::-1]

        self.dims = self.q_dims + self.p_dims[1:]

        self.lam = self.alg_cfg['lambda']
        self.lr = self.alg_cfg['lr']
        self.random_seed = self.alg_cfg['random_seed']

        self.construct_placeholders()

    def construct_placeholders(self):
        self.input_ph = tf.placeholder(
            dtype=tf.float32, shape=[None, self.dims[0]])
        self.keep_prob_ph = tf.placeholder_with_default(1.0, shape=None)

    def build_graph(self):
        self.construct_weights()

        saver, logits = self.forward_pass()
        log_softmax_var = tf.nn.log_softmax(logits)

        # per-user average negative log-likelihood
        neg_ll = -tf.reduce_mean(tf.reduce_sum(
            log_softmax_var * self.input_ph, axis=1))
        # apply regularization to weights
        reg = l2_regularizer(self.lam)
        reg_var = apply_regularization(reg, self.weights)
        # tensorflow l2 regularization multiply 0.5 to the l2 norm
        # multiply 2 so that it is back in the same scale
        loss = neg_ll + 2 * reg_var

        train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)

        # add summary statistics
        tf.summary.scalar('negative_multi_ll', neg_ll)
        tf.summary.scalar('loss', loss)
        merged = tf.summary.merge_all()
        return saver, logits, loss, train_op, merged

    def forward_pass(self):
        # construct forward graph
        h = tf.nn.l2_normalize(self.input_ph, 1)
        h = tf.nn.dropout(h, self.keep_prob_ph)

        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            h = tf.matmul(h, w) + b

            if i != len(self.weights) - 1:
                h = tf.nn.tanh(h)
        return tf.train.Saver(), h

    def construct_weights(self):
        self.weights = []
        self.biases = []

        # define weights
        for i, (d_in, d_out) in enumerate(zip(self.dims[:-1], self.dims[1:])):
            weight_key = "weight_{}to{}".format(i, i + 1)
            bias_key = "bias_{}".format(i + 1)

            self.weights.append(tf.get_variable(
                name=weight_key, shape=[d_in, d_out],
                initializer=tf.glorot_normal_initializer(
                    seed=self.random_seed)))

            self.biases.append(tf.get_variable(
                name=bias_key, shape=[d_out],
                initializer=tf.truncated_normal_initializer(
                    stddev=0.001, seed=self.random_seed)))

            # add summary stats
            tf.summary.histogram(weight_key, self.weights[-1])
            tf.summary.histogram(bias_key, self.biases[-1])

    @staticmethod
    def NDCG_binary_at_k_batch(X_pred, heldout_batch, k=100):
        '''
        normalized discounted cumulative gain@k for binary relevance
        ASSUMPTIONS: all the 0's in heldout_data indicate 0 relevance
        '''
        batch_users = X_pred.shape[0]
        idx_topk_part = bn.argpartition(-X_pred, k, axis=1)
        topk_part = X_pred[np.arange(batch_users)[:, np.newaxis],
                           idx_topk_part[:, :k]]
        idx_part = np.argsort(-topk_part, axis=1)
        # X_pred[np.arange(batch_users)[:, np.newaxis], idx_topk] is the sorted
        # topk predicted score
        idx_topk = idx_topk_part[np.arange(batch_users)[:, np.newaxis], idx_part]
        # build the discount template
        tp = 1. / np.log2(np.arange(2, k + 2))

        DCG = (heldout_batch[np.arange(batch_users)[:, np.newaxis],
                             idx_topk].toarray() * tp).sum(axis=1)
        IDCG = np.array([(tp[:min(n, k)]).sum()
                         for n in heldout_batch.getnnz(axis=1)])
        return DCG / IDCG

    @staticmethod
    def Recall_at_k_batch(X_pred, heldout_batch, k=100):
        batch_users = X_pred.shape[0]

        idx = bn.argpartition(-X_pred, k, axis=1)
        X_pred_binary = np.zeros_like(X_pred, dtype=bool)
        X_pred_binary[np.arange(batch_users)[:, np.newaxis], idx[:, :k]] = True

        X_true_binary = (heldout_batch > 0).toarray()
        tmp = (np.logical_and(X_true_binary, X_pred_binary).sum(axis=1)).astype(
            np.float32)
        recall = tmp / np.minimum(k, X_true_binary.sum(axis=1))
        return recall

    def execute_training(self):
        idxlist = list(self.data.tr_dict.keys())
        N = len(idxlist)
        batch_size = self.alg_cfg['batch_size']
        batches_per_epoch = int(np.ceil(float(N) / batch_size))
        idxlist_val = list(self.data.val_tr_dict.keys())
        N_val = len(idxlist_val)
        batch_size_val = self.alg_cfg['batch_size_val']
        total_anneal_steps = self.alg_cfg['tot_anneal_steps']
        anneal_cap = self.alg_cfg['anneal_cap']

        # Train a multiDae
        self.lam = self.alg_cfg['lambda'] / self.alg_cfg['batch_size']
        saver, logits_var, loss_var, train_op_var, merged_var = self.build_graph()

        ndcg_var = tf.Variable(0.0)
        ndcg_dist_var = tf.placeholder(dtype=tf.float64, shape=None)
        ndcg_summary = tf.summary.scalar('ndcg_at_k_validation', ndcg_var)
        ndcg_dist_summary = tf.summary.histogram('ndcg_at_k_hist_validation', ndcg_dist_var)
        merged_valid = tf.summary.merge([ndcg_summary, ndcg_dist_summary])

        arch_str = "I-%s-I" % ('-'.join([str(d) for d in self.dims[1:-1]]))

        log_dir = './log/Ml-20m/DAE/{}'.format(arch_str)

        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)

        # print("log directory: %s" % log_dir)
        summary_writer = tf.summary.FileWriter(log_dir, graph=tf.get_default_graph())

        chkpt_dir = './chkpt/Ml-20m/DAE/{}'.format(arch_str)

        if not os.path.isdir(chkpt_dir):
            os.makedirs(chkpt_dir)

        n_epochs = self.alg_cfg['n_epochs']
        ndcgs_vad = []

        with tf.Session() as sess:

            init = tf.global_variables_initializer()
            sess.run(init)
            best_ndcg = -np.inf

            for epoch in range(n_epochs):
                np.random.shuffle(idxlist)
                # train for one epoch
                for bnum, st_idx in enumerate(range(0, N, batch_size)):
                    end_idx = min(st_idx + batch_size, N)
                    X = self.data.tr_matr[idxlist[st_idx:end_idx]]

                    if sparse.isspmatrix(X):
                        X = X.toarray()
                    X = X.astype('float32')

                    feed_dict = {self.input_ph: X,
                                 self.keep_prob_ph: 0.5}
                    sess.run(train_op_var, feed_dict=feed_dict)

                    if bnum % 100 == 0:
                        summary_train = sess.run(merged_var, feed_dict=feed_dict)
                        summary_writer.add_summary(summary_train, global_step=epoch * batches_per_epoch + bnum)
                # compute validation NDCG
                ndcg_dist = []
                for bnum, st_idx in enumerate(range(0, N_val, batch_size_val)):
                    end_idx = min(st_idx + batch_size_val, N_val)
                    X = self.data.val_tr_matr[idxlist_val[st_idx:end_idx]]

                    if sparse.isspmatrix(X):
                        X = X.toarray()
                    X = X.astype('float32')

                    pred_val = sess.run(logits_var, feed_dict={self.input_ph: X})
                    # exclude examples from training and validation (if any)
                    pred_val[X.nonzero()] = -np.inf
                    ndcg_dist.append(self.NDCG_binary_at_k_batch(pred_val, self.data.val_te_matr[idxlist_val[st_idx:end_idx]]))

                ndcg_dist = np.concatenate(ndcg_dist)
                ndcg_ = ndcg_dist.mean()
                ndcgs_vad.append(ndcg_)
                merged_valid_val = sess.run(merged_valid, feed_dict={ndcg_var: ndcg_, ndcg_dist_var: ndcg_dist})
                summary_writer.add_summary(merged_valid_val, epoch)

                # update the best model (if necessary)
                if ndcg_ > best_ndcg:
                    saver.save(sess, '{}/model'.format(chkpt_dir))
                    best_ndcg = ndcg_

        idxlist_test = list(self.data.test_tr_dict.keys())
        N_test = len(idxlist_test)
        batch_size_test = self.alg_cfg['batch_size_test']
        chkpt_dir = './chkpt/Ml-20m/DAE/{}'.format(arch_str)
        entire_pred_matr = self.data.test_tr_matr[idxlist_test]
        with tf.Session() as sess:
            saver.restore(sess, '{}/model'.format(chkpt_dir))

            for bnum, st_idx in enumerate(range(0, N_test, batch_size_test)):
                end_idx = min(st_idx + batch_size_test, N_test)
                X = self.data.test_tr_matr[idxlist_test[st_idx:end_idx]]

                if sparse.isspmatrix(X):
                    X = X.toarray()
                X = X.astype('float32')

                pred_val = sess.run(logits_var, feed_dict={self.input_ph: X})
                # exclude examples from training and validation (if any)
                pred_val[X.nonzero()] = -np.inf
                # entire_pred_matr[idxlist_test[st_idx:end_idx]] = pred_val
                entire_pred_matr[st_idx:end_idx] = pred_val
            return entire_pred_matr

    def prediction(self, all_ratings):
        return [all_ratings[u].toarray()[0] for u in range(all_ratings.shape[0])]




