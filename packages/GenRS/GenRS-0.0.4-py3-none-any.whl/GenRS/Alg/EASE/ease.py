from GenRS.Alg.alg import Alg
import numpy as np

class Ease(Alg):
    def __init__(self, data, alg_cfg):
        super().__init__(data)
        self.alg_cfg = alg_cfg
        self.lam = self.alg_cfg['lambda']

    def execute_training(self):
        X = self.data.whole_tr_matr.todense()
        G = np.dot(X.T, X)
        diag_ind = np.diag_indices(G.shape[0])
        G[diag_ind] += self.lam
        P = np.linalg.inv(G)
        del G
        B = P / (-np.diag(P))
        B[diag_ind] = 0

        return B

    def prediction(self, all_ratings):
        X = self.data.whole_tr_matr.todense()
        S = np.dot(X, all_ratings)
        S[X.nonzero()] = -np.inf
        S = S[self.data.test_te_us]
        c = [v[0] for v in S]
        a = []
        for i in range(len(self.data.test_te_us)):
          a.append(np.array(c[i])[0])
        return a
