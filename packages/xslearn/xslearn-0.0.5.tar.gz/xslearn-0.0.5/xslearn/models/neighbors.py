from .base import BaseModel
import numpy as np



class KNeighborsClassifier(BaseModel):
    def __init__(self, k=3, p=2):
        super(KNeighborsClassifier, self).__init__()
        self.k = k
        self.p = p
        self.X = None
        self.y = None


    def fit(self, X, y):
        self.X = X
        self.y = y
        super(KNeighborsClassifier, self).fit()


    def calc_dist(self, x1, x2):
        if x1.ndim == 1:
            x1 = np.expand_dims(x1, axis=0)
        if x2.ndim == 1:
            x2 = np.expand_dims(x2, axis=0)
        x1 = x1[:, np.newaxis, :]
        x2 = x2[np.newaxis, :]
        dist = np.power(np.sum(np.abs(x1 - x2) ** self.p, axis=2), 1 / self.p)
        return dist


    def predict(self, X, is_train=False, *args):
        X = np.asarray(X)
        dist = self.calc_dist(X, self.X)
        closet_index = np.argsort(dist, axis=1)[:, :self.k]
        closet_label = self.y[closet_index]
        majority_label = np.zeros((X.shape[0], 1))
        for i in range(len(closet_label)):
            t = closet_label[i].tolist()
            majority_label[i] = max(t, key=t.count)
        return majority_label



