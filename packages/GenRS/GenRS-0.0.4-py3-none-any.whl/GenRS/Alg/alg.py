from collections import defaultdict
import numpy as np


class Alg:

    def __init__(self, data):
        self.data = data

    def execute_training(self):
        pass

    def prediction(self, all_ratings):
        pass

    def save_training(self, saver, sess, save_path="./model.ckpt"):
        pass

    def load_training(self):
        pass
