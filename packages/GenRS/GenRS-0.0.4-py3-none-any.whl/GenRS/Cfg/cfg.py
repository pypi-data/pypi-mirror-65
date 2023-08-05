import sys
import json


# Configuration class
class Cfg:

    def __init__(self):
        pass

    @staticmethod
    def load_conf(path="./cfg.JSON"):
        """
        :param path: path to main configuration file
        :return settings:  it contains information about the dataset (seed, train size, validation, paths,...)
        """
        with open(path) as conf_file:
            settings = json.load(conf_file)
        return settings


# Framework configuration class
class FrmCfg(Cfg):

    def __init__(self, path="./cfg.JSON"):
        super().__init__()
        self.__dict__ = self.load_conf(path)  # in this way we can access directly to each field of cfg.JSON file

    def save_conf(self, path="./Saved/cfg.JSON"):
        """
        :param path: where the conf will be saved
        """
        with open(path, 'w+') as conf_file:     # TODO change it in order to write a file loaded by the load_conf function
            json.dump(self.__dict__, conf_file)


# Alg configuration class
class AlgCfg(Cfg):

    def __init__(self, algo, cfg_path=None):
        """
        :param algo: name of the algorithm to load config
        :param cfg_path: path to hyperparams
        """
        super().__init__()
        self.algo = algo
        if cfg_path is None:
            cfg_path = "./{}_cfg.JSON".format(algo)
        self.cfg = self.load_conf(cfg_path)

    def save_conf(self, path=None):
        if path is None:
            path = "./../Cfg/Saved/{}_cfg.JSON".format(self.algo)

        with open(path, 'w+') as conf_file:     # TODO change it in order to write a file loaded by the load_conf function
            json.dump(self.__dict__, conf_file)


