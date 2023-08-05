import copy
import logging
import os
from collections import defaultdict
from time import time

import numpy as np
import pandas as pd
from scipy import sparse


class Reader:

    def __init__(self, settings):
        """
        :param settings: FrmCfg instance
        """
        logging.basicConfig(filename=settings.out_log)

        self.settings = settings  # you have access to all fields in settings through self.settings.field_name
        # t1 = time()
        self.df = self.load_data(settings.path, settings.sep, settings.names)  # load dataset containing data
        if settings.preproc_data:
            filt_df = self.filt_data(self.df, threshold=settings.min_rat, min_uc=settings.min_uc, min_sc=settings.min_sc)

            self.n_us, self.n_it, us_e2i, it_e2i = self.create_mapping(filt_df)
            self.df = self.apply_encoding(filt_df, us_e2i,
                                          it_e2i)  # create the new df encoded with only user, item columns
            if settings.write_set:
                self.write_filtered_data(self.df, f_path="./preproc_data.csv", sep=settings.sep)
        else:
            col0, col1 = list(self.df)[0:2]
            self.n_us, self.n_it = len(pd.unique(self.df[col0])), len(pd.unique(self.df[col1]))

    def filt_data(self, df, threshold=0, min_uc=0, min_sc=0):
        """
        :param df: pandas DataFrame that has to be filter
        :param threshold: minimum considered rating value in df
        :param min_uc: maintain only the user that rate at least min_uc items
        :param min_sc: maintain only the items that has been rated at least by min_sc user
        :return df: the pandas DataFrame df after users and items filtering
        """
        df = self.filter_by_rat(df, threshold)
        df = self.filt_us_it(df, min_uc, min_sc)
        return df

    @staticmethod
    def load_data(data_path, sep=None, names=None, index_col=None):
        """
        :param data_path: path of dataset file
        :param sep: separator used in dataset file to split user item columns
        :param names: column names of the dataframe
        :param index_col: bool: true if index_column is in data_path
        :return pandas DataFrame data built from the reading of the file
        """

        if sep is None:
            sep = ','
        try:
            data = pd.read_csv(data_path, names=names, sep=sep, index_col=index_col, dtype=float, usecols=[0, 1, 2])
            if data.empty:
                logging.fatal(
                    "Error! The path you've inserted into cfg.JSON file does NOT contains data. Check it out!")
                exit(1)
            return data
        except FileNotFoundError:
            logging.fatal("ERROR! No file found in {}".format(data_path))
            exit(1)

    @staticmethod
    def filter_by_rat(df, threshold=3):
        """
        :param df: pandas DataFrame
        :param threshold: minimum considered value in df
        :return: the pandas DataFrame with filtered ratings
        """
        rat_col = list(df)[2]
        df = df[df[rat_col] >= threshold]
        return df

    @staticmethod
    def encode_user(user_e2i, x):
        """
        This function is used to encoding the explicit value of users to the implicit
        :param x: user that has to be mapped
        :param user_e2i: dict used for user's encoding
        :return us: encoded user
        """
        return user_e2i[x]

    @staticmethod
    def encode_item(item_e2i, i):
        """
        This function is used to encoding the explicit value of items to the implicit
        :param item_e2i: dict used for item's encoding
        :param i: item that has to be mapped
        :return it: encoded item
        """
        return item_e2i[i]

    @staticmethod
    def get_count(df, col_id):
        """
        :param df: encoded pandas Dataframe
        :param col_id: name of the column in df
        :return count: number of different values in col_id of df
        """
        list_unique_id = df[[col_id]].groupby(col_id, as_index=False)
        count = list_unique_id.size()
        return count

    def filt_us_it(self, df, min_uc=0, min_sc=0):
        """
        :param df: pandas DataFrame
        :param min_uc: maintain only the user that rate at least min_uc items
        :param min_sc: maintain only the items that has been rated at least by min_sc user
        :return df: the pandas DataFrame df after users and items filtering
        """
        col0, col1 = list(df)[:2]
        # Only keep the data for items which were clicked on by at least min_sc users.
        if min_sc > 0:
            it_ = self.get_count(df, col1)
            df = df[df[col1].isin(it_.index[it_ >= min_sc])]

        # Only keep the data for users who clicked on at least min_uc items
        # After doing this, some of the items will have less than min_uc users, but should only be a small proportion
        if min_uc > 0:
            us_ = self.get_count(df, col0)
            df = df[df[col0].isin(us_.index[us_ >= min_uc])]

        return df[list(df)[0:2]]

    def apply_encoding(self, df, us_e2i, it_e2i):
        """
        :param df: original pandas dataframe on which we want to apply the encoding
        :param us_e2i: map explicit user to implicit id
        :param it_e2i: map explicit item to implicit id
        :return enc_df: df encoded with only the user and item columns filled with us_ids and item_ids
        """
        enc_df = pd.DataFrame()
        col0, col1 = list(df)[:2]  # get first two columns of dataframe data
        enc_df[col0] = df[col0].transform(lambda x: self.encode_user(us_e2i, x))  # encode users to implicit ids
        enc_df[col1] = df[col1].transform(lambda x: self.encode_item(it_e2i, x))  # encode items to implicit ids
        return enc_df

    @staticmethod
    def create_mapping(df):
        """
        :param df: DataFrame we want to map
        :param user_e2i: user dictionary that map each explicit id to an implicit
        :param item_e2i: item dictionary that map each explicit id to an implicit
        :return user_e2i, item_e2i: dictionaries that map each explicit user and item id through a new id (implicit)
        :return n_us, n_it: number of user and items in the updated DataFrame
        """

        us_col, it_col = list(df)[0:2]

        unique_uid = pd.unique(df[us_col])
        unique_iid = pd.unique(df[it_col])

        us_e2i = dict((uid, i) for (i, uid) in enumerate(unique_uid))
        it_e2i = dict((iid, i) for (i, iid) in enumerate(unique_iid))

        n_us, n_it = len(unique_uid), len(unique_iid)

        return n_us, n_it, us_e2i, it_e2i

    @staticmethod
    def write_filtered_data(df, f_path=None, sep=None, new_col_names=None):
        """
        It takes preprocessed dataframe and save the first two columns on file
        specified in f_path variable
        :param df: DataFrame to save
        :param f_path: string containing the path
        :param sep: separator of csv file
        :param new_col_names: list of 2 strings: default is ["user_id", "item_id"]
        """
        if new_col_names is None:
            new_col_names = ["user_id", "item_id"]
        assert len(new_col_names) == 2 and all(
            isinstance(x, str) for x in new_col_names), "The parameter new_col_names must be a list of two strings"

        if f_path is None:
            f_path = "./output.csv"

        if sep is None:
            sep = ','
        assert isinstance(sep, str), "The sep parameter must be a string."
        if len(list(df)) > 2:
            df = df[list(df)[0:2]]

        df.to_csv(f_path, header=new_col_names, sep=sep, index=False)


class DataManager:

    def __init__(self, data):
        """
        :param data: a Reader instance
        """
        self.data = data
        self.n_us, self.n_it = data.n_us, data.n_it
        # self.sparsity = 1. * data.df.shape[0] / (data.n_us * data.n_it)
        self.col0, self.col1 = list(data.df)[0:2]
        df = data.df
        path_files = ["./train.csv", "./val_tr.csv", "./val_te.csv", "./test_tr.csv", "./test_te.csv"]
        if data.settings.create_tr_val_test:
            uid = np.arange(self.n_us)
            iid = np.arange(self.n_it)

            rand_uid = self.list_randomizer(uid, seed=self.data.settings.seed)

            # split train, val and test through users
            tr_us, self.val_us, self.test_us = self.split_us(rand_uid, heldout_us_val=self.data.settings.heldout_us_val,
                                                             heldout_us_test=self.data.settings.heldout_us_test)

            # build tr, val and test DataFrame
            self.tr = df.loc[df[self.col0].isin(tr_us)]
            # assert (val not in self.test_us for val in self.val_us), exit(1)
            self.val = self.create_sub_df(df, self.val_us, iid)
            self.test = self.create_sub_df(df, self.test_us, iid)

            self.val_tr, self.val_te = self.split_tr_test_items(self.val, self.data.settings.test_it_prop,
                                                                self.data.settings.seed)
            self.test_tr, self.test_te = self.split_tr_test_items(self.test, self.data.settings.test_it_prop,
                                                                  self.data.settings.seed)

            all_df = [self.tr, self.val_tr, self.val_te, self.test_tr, self.test_te]

            for i in range(len(path_files)):
                all_df[i].to_csv(path_files[i], header=["user_id", "item_id"], sep=',')

        sp_matr_list = []
        for i in range(len(path_files)):
            sp_matr_list.append(self.load_sp_matr(path_files[i], self.n_us, self.n_it))
        self.tr_matr, self.val_tr_matr, self.val_te_matr, self.test_tr_matr, self.test_te_matr = sp_matr_list

        # create the dictionaries starting from the sparse matrices
        dict_list = []
        for i in range(len(sp_matr_list)):
            dict_list.append(self.make_dict(sp_matr_list[i]))

        self.tr_dict, self.val_tr_dict, self.val_te_dict, self.test_tr_dict, self.test_te_dict = dict_list
        # in case of no validation process, whole_tr= tr + entire val + test_tr
        self.whole_tr_matr = self.tr_matr + self.val_tr_matr + self.val_te_matr + self.test_tr_matr

        self.test_te_us = np.unique(sparse.find(self.test_te_matr)[0])     # array with the test_te users

        self.gt = self.test_te_dict
        self.gt_array = list(self.gt.values())

    @staticmethod
    def load_sp_matr(path, m, n):
        """
        Return an m x n csr_matrix from path file
        ------------
        :param path: file .csv to read
        :param m: num of rows returned
        :param n: num of cols returned
        :return csr_matrix: m x n sparse_matrix
        """
        data = pd.read_csv(path)
        rows, cols = data['user_id'], data['item_id']
        return sparse.csr_matrix((np.ones_like(rows), (rows, cols)), dtype='int32', shape=(m, n))

    @staticmethod
    def make_dict(sp_matr):
        """
        create dictionary from csr_matrix
        -----------
        :param sp_matr: sparse csr_matrix
        :return a dictionary with as key the rows and values the indices of items different from 0 in sp_matr
        """
        return {u: list(d.nonzero()[1]) for u, d in enumerate(sp_matr) if len(list(d.nonzero()[1])) > 0}

    @staticmethod
    def list_randomizer(unique_uid, seed=0):
        """
        Randomize the elements of the list
        ----------------
        :param unique_uid: list of unique user id
        :param seed: seed used
        :return a randomized list containing unique_uid elements
        """
        np.random.seed(seed)
        idx_perm = np.random.permutation(unique_uid.size)
        unique_uid = unique_uid[idx_perm]
        return unique_uid

    @staticmethod
    def split_us(unique_uid, heldout_us_val=1, heldout_us_test=1):
        """
        Split the users into three different sets
        ---------------------
        :param unique_uid: num of unique user_ids
        :param heldout_us_val: num of user to keep in val_set
        :param heldout_us_test: num of user to keep in test_set
        :return tr_us: users used in tr_set
        :return val_us: users used in val_set
        :return test_us: users used in test_set
        """
        n_us = unique_uid.size

        assert isinstance(heldout_us_val, int), "Error in Framework configuration.\n " \
                                                "The heldout_us_val parameter in cfg.JSON" \
                                                " must be an integer greater than 0."

        assert (heldout_us_val <= int(0.5 * n_us)), "Error in Framework configuration.\n" \
                                                   "The heldout_us_val parameter in cfg.JSON" \
                                                   "is too much high. Reduce it"
        assert (heldout_us_val > 0), "Error in Framework configuration.\n " \
                                                "The heldout_us_val parameter in cfg.JSON" \
                                                " must be an integer greater than 0."

        assert isinstance(heldout_us_test, int), "Error in Framework configuration.\n " \
                                                "The heldout_us_test parameter in cfg.JSON" \
                                                " must be an integer greater than 0."
        assert (heldout_us_test <= int(0.5 * n_us)), "Error in Framework configuration.\n" \
                                                   "The heldout_us_test parameter in cfg.JSON" \
                                                   "is too much high. Reduce it"
        assert (heldout_us_test > 0), "Error in Framework configuration.\n " \
                                     "The heldout_us_val parameter in cfg.JSON" \
                                     " must be an integer greater than 0."

        tr_us = unique_uid[:(n_us - heldout_us_val - heldout_us_test)]
        val_us = unique_uid[(n_us - heldout_us_val - heldout_us_test): (n_us - heldout_us_test)]
        test_us = unique_uid[(n_us - heldout_us_test):]

        return tr_us, val_us, test_us

    @staticmethod
    def split_tr_test_items(data, test_prop=0.2, seed=0):
        """
        Split data into training and test subset based on items.
        ------------------
        :param data: pandas DataFrame
        :param test_prop: portion of items that has to be set in test set
        :param seed: seed for random
        :return train_subset: subset of data that maintain only a subset of item
        :return test_subset: subset of data that maintain the
        """
        data_grouped_by_user = data.groupby(list(data)[0])
        tr_list, te_list = list(), list()

        np.random.seed(seed)

        for i, (_, group) in enumerate(data_grouped_by_user):
            n_items_u = len(group)

            if n_items_u >= 5:      # min 5 items rated by users to be main
                idx = np.zeros(n_items_u, dtype='bool')
                idx[np.random.choice(n_items_u, size=int(test_prop * n_items_u), replace=False).astype('int64')] = True

                tr_list.append(group[np.logical_not(idx)])
                te_list.append(group[idx])
            else:
                tr_list.append(group)

        data_tr = pd.concat(tr_list)
        data_te = pd.concat(te_list)

        return data_tr, data_te

    @staticmethod
    def create_sub_df(df, list_us, unique_iid):
        """
        Create training, validation or test set, starting from a list of users that contains only the item indices in unique_iid
        ------------------
        :param df: pandas DataFrame
        :param list_us: list of selected users
        :param unique_iid: list of unique item ids
        :return data: DataFrame composed by the users in list_us that have items in unique_iid
        """
        data = df.loc[df[list(df)[0]].isin(list_us)]        # maintain only the selected user from original df
        data = data.loc[data[list(df)[1]].isin(unique_iid)]     # maintain only the items in unique_iid list that have been rated by the users in list_us
        return data



