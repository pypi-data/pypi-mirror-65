from collections import defaultdict
import numpy as np


class Alg:

    def __init__(self, data):
        """
        Superclass of algorithms
        @param data: DataManager instance, it contains all the useful data structure
        """
        self.data = data

    def execute_training(self):
        pass

    def prediction(self, pred_matr):
        """
        Compute prediction over csr_matrix with test_us by n_items
        -----------
        @param pred_matr: sparse matrix with prediction ratings in sparse csr_matrix form
        @return: list of array with ordered indices
        """
        assert pred_matr.shape[0] == self.data.data.settings.heldout_us_test, \
            "The shape of prediction matrix must be {} by {}. Check it out".format(self.data.data.settings.heldout_us_test, self.data.n_it)
        c = [pred_matr[u].toarray()[0] for u in range(pred_matr.shape[0])]
        pred_ord = []
        for j in range(len(c)):
            pred_ord.append(self.sort_(c[j]))
        return pred_ord

    def save_training(self, saver, sess, save_path="./model.ckpt"):
        pass

    def load_training(self):
        pass

    @staticmethod
    def sort_(unsort_list, dec=True):
        """
        Returns the ordered indices sorted by value
        --------------
        @param unsort_list: the list to sort
        @type unsort_list: list of integers
        @param dec: whether to sort in descending order or not
        @type dec: boolean (default: True)
        """
        d = {k: unsort_list[k] for k in range(len(unsort_list))}
        return sorted(d.keys(), key=lambda s: d[s], reverse=dec)
