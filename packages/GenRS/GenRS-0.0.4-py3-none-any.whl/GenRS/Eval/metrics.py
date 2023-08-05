import logging
from collections import defaultdict
import math

import numpy as np


class Metrics:
    def __init__(self, metrics, gt, pred):
        """
        :param metrics: list of metrics
        :param gt: set list of indices of real users preferences
        :param pred: array-list of indices (predicted values) returned by algorithm
        """
        self.dict_metrics = self.compute_metrics(metrics, gt, pred)

    # ignore the pycharm advice to render this method static
    def compute_metrics(self, metrics, gt, pred):
        """
        Returns a defaultdict in the form <metr_name: value> containing all metrics
        :param metrics: list of metrics
        :param gt: set list of indices of real users preferences
        :param pred: array-list of indices (predicted values) returned by algorithm
        :return dict_metrics: defaultdict in the form <metr_name: value>
        """
        dict_metrics = defaultdict(float)
        for metr_name in metrics:
            at = metr_name.split('@')        # merge metr_name to get k value if @ in metr_name
            if len(at) > 1:     # Positive case: @ in metr_name
                k = int(at[1])      # get k value
                counter = 0.
                for i, (key, val) in enumerate(gt.items()):
                    counter += getattr(self, '{}'.format(at[0]))(gt[key], pred[i], k)   # call the right metric with k as param and update the dict
                dict_metrics[metr_name] = counter / len(gt)
            else:
                counter = 0.
                for i, (key, val) in enumerate(gt.items()):
                    counter += getattr(self, '{}'.format(at[0]))(gt[key], pred[i])        # call the metric and update the dict
                dict_metrics[metr_name] = counter / len(gt)

        return dict_metrics

    def ndcg(self, gt, pred, k):
        """
        Calculates the normalized discounted cumulative gain at k
        ------------------------
        :param gt: set of indices considering real user preferences
        :param pred: array of indices considering the predicted user preference
        :param k: cutoff threshold
        :return ndcg@k: normalized discounted cumulative gain @k
        """
        k = min(k, len(pred))
        idcg = self.idcg(k)
        dcg_k = sum([int(pred[i] in gt) / math.log(i + 2, 2) for i in range(k)])
        return dcg_k / idcg

    @staticmethod
    def idcg(k):
        """
        Calculates the ideal discounted cumulative gain at k
        ------------------------
        :param k: cutoff threshold
        :return idcg@k: ideal discounted cumulative gain @k
        """
        res = sum([1.0 / math.log(i + 2, 2) for i in range(k)])
        if not res:
            return 1.0
        else:
            return res

    @staticmethod
    def precision(gt, pred, k):
        """
        Precision@k = (# of recommended items @k that are relevant) / (# of recommended items @k)
        ---------------------------
        :param gt: set of indices considering real user preferences
        :param pred: array of indices considering the predicted user preference
        :param k: cutoff threshold
        :return P@k: precision@k
        """
        k = min(len(pred), k)
        den = min(len(gt), k)
        return sum([int(pred[i] in gt) for i in range(k)]) / den


    @staticmethod
    def recall(gt, pred, k):
        """
        Recall@k = (# of recommended items @k that are relevant) / (# of relevant items)
        :param gt: set of indices considering real user preferences
        :param pred: array of indices considering the predicted user preference
        :param k: cutoff threshold
        :return R@k: recall@k
        """
        k = min(len(pred), k)
        return sum([int(pred[i] in gt) for i in range(k)]) / len(gt)

    @staticmethod
    def ap(gt, pred, k):
        """
        Calculates the average precision at k
        ------------------------
        :param gt: set of indices considering real user preferences
        :param pred: array of indices considering the predicted user preference
        :param k: cutoff threshold
        :return ap@k: average precision @k
        """
        if len(pred) > k:
            pred = pred[:k]

        score = 0.0
        num_hits = 0.0

        for i, p in enumerate(pred):
            if p in gt:
                num_hits += 1.0
                score += num_hits / (i + 1.0)

        if not gt:
            return 0.

        return score / min(len(gt), k)

    @staticmethod
    def auc(gt, pred):
        """
        Calculates AUC
        --------------------
        :param gt: set of indices considering real user preferences
        :param pred: array of indices considering the predicted user preference
        """
        np_ = len(gt)
        n = len(pred)
        area = 0.0

        for i in range(n):
            if pred[i] in gt:
                for j in range(i + 1, n):
                    if pred[j] not in gt:
                        area += 1.0

        area /= float(np_ * (n - np_))
        return area

