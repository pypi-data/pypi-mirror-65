import sys
import json
import logging
from GenRS.Cfg.cfg import FrmCfg, AlgCfg
from GenRS.Data.data_manager import DataManager, Reader
from GenRS.Alg.alg import Alg
from GenRS.Eval.metrics import Metrics
import importlib
from time import time


class RecSys:

    def __init__(self, path_cfg="./cfg.JSON", path_algos=None):
        """
        Execute the whole recommendation pipeline
        ------------
        @param path_cfg: path of framework configuration file
        @param path_algos: list of path to algo configuration file
        """
        
        t1 = time()
        settings = FrmCfg(path_cfg)  # from now on we can use settings.name_of_par to access it
        # settings.save_conf()
        if settings.out_log is None:
            logging.basicConfig(filename="./console.log.txt", level=logging.DEBUG)
        else:
            logging.basicConfig(filename=settings.out_log, level=logging.DEBUG)

        if path_algos is None:
            path_algos = ["{}_cfg.JSON".format(alg) for alg in settings.algos]
        reader = Reader(settings)

        data = DataManager(reader)
        t2 = time()
        logging.log(level=logging.DEBUG, msg="{} seconds used for loading and preprocess data".format(t2-t1))
        algorithms = settings.algos

        for i, algo in enumerate(algorithms):

            algo_settings = AlgCfg(algo, path_algos[i])
            algo_class = getattr(importlib.import_module("GenRS.Alg.{}.{}".format(algo.upper(), algo)),
                                 "{}".format(algo.capitalize()), self.get_new_alg(algo))
            algor = algo_class(data, algo_settings.cfg)
            all_rat = algor.execute_training()
            pred_ord = algor.prediction(all_rat)

            results = Metrics(settings.metrics, data.target, pred_ord)       # compute metrics

            for key, val in results.dict_metrics.items():
                logging.log(level=logging.DEBUG, msg="{}={}".format(key, val))


    def get_new_alg(self, algo_name):
        """
        Load the new algorithm class to use for prediction
        -----------------------
        @param algo_name: name of algorithm class to import
        @return:
        """
        pass

