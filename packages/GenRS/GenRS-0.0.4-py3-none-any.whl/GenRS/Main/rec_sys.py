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
        @param path_cfg: path of framework configuration file
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

            algo_settings = AlgCfg(algo, path_algos[i])    # evaluate if keep
            algo_class = getattr(importlib.import_module("GenRS.Alg.{}.{}".format(algo.upper(), algo)), "{}".format(algo.capitalize()))
            algor = algo_class(data, algo_settings.cfg)
            t3 = time()
            pred_ = algor.execute_training()
            t4 = time()
            logging.log(level=logging.DEBUG, msg="{} seconds used for the training phase".format(t4 - t3))
            pred_ = algor.prediction(pred_)

            # Preprocess predicted data before evaluation phase
            pred_ord = []
            for j in range(len(data.gt_array)):
                pred_ord.append(sort_(pred_[j], skip=[]))
            target = {}
            for j in list(data.gt.keys()):
                target[j] = set(data.gt[j])     # unordered: what matters is the presence of item index, not the position

            results = Metrics(settings.metrics, target, pred_ord)       # compute metrics

            for key, val in results.dict_metrics.items():
                logging.log(level=logging.DEBUG, msg="{}={}".format(key, val))


# Sorts the list by value
def sort_(unsort_list, skip, dec=True):
    """
    Returns the ordered indices sorted by value
    --------------
    @param unsort_list: the list to sort
    @type unsort_list: list of integers
    @param skip: list of indexes to skip
    @type skip: list of int
    @param dec: whether to sort in descending order or not
    @type dec: boolean (default: True)
    """
    d = {k: unsort_list[k] for k in range(len(unsort_list)) if k not in skip}
    return sorted(d.keys(), key=lambda s: d[s], reverse=dec)
