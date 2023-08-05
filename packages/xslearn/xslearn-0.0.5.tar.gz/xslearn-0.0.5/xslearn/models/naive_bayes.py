from .base import *


class NaiveBayes(BaseModel):
    def __init__(self, Lambda=0):
        super(NaiveBayes, self).__init__()
        self.X = None
        self.y = None
        self.Lambda = Lambda
        self.label_dict = None
        self.n_sample = None


    def fit(self, X, y):
        self.label_dict = self.generateLabelDict(y)
        self.X = np.array(X)
        self.y = np.array(y)
        self.n_sample = X.shape[0]
        super(NaiveBayes, self).fit()


    def predict(self, X, is_train=False, *args):
        X = np.array(X)
        if X.ndim == 1:
            X = np.expand_dims(X, 0)
        pred_label_dict = {}
        K = len(self.label_dict.keys())
        # calculate P(y = c_k)
        for label, val in self.label_dict.items():
            p = (val + self.Lambda) / (self.n_sample + K * self.Lambda)
            label_idx_in_y = np.where(self.y == label)
            label_data = self.X[label_idx_in_y]
            # iter every attr's value
            for i, attr in enumerate(X[0]):
                s_j = len(set(self.X[:, i]))
                attr_data = np.where(label_data[:, i] == attr)[0]
                p *= (len(attr_data) + self.Lambda) / (len(label_idx_in_y) + s_j * self.Lambda)

            pred_label_dict[label] = p

        max_p = -1
        p_label = None
        for label, p in pred_label_dict.items():
            if p > max_p:
                p_label = label
                max_p = p
        return p_label



    def generateLabelDict(self, y):
        label_dict = {}
        for label in y:
            if label in label_dict:
                label_dict[label] += 1
            else:
                label_dict[label] = 0
        return label_dict




class GaussianNaiveBayes(BaseModel):
    def __init__(self):
        super(GaussianNaiveBayes, self).__init__()
        self.X = None
        self.y = None
        self.label_dict = None
        self.n_sample = None


    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.label_dict = self.generateLabelDict(y)
        self.X = X
        self.y = y
        self.n_sample = X.shape[0]
        super(GaussianNaiveBayes, self).fit()


    def predict(self, X, is_train=False, *args):
        X = np.array(X)
        if X.ndim > 1 and X.shape[0] >= 1:
            pred = np.zeros((X.shape[0], 1))
            for j, x in enumerate(X):
                pred_label_dict = {}
                # calculate P(y = c_k)
                for label, val in self.label_dict.items():
                    p = val / self.n_sample
                    label_idx_in_y = np.where(self.y == label)
                    label_data = self.X[label_idx_in_y]
                    # iter every attr's value
                    for i, attr in enumerate(x):
                        mean, var = self.calc_mean_var(label_data[:, i])
                        p_xi_c = np.exp(-(attr - mean) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
                        p *= p_xi_c

                    pred_label_dict[label] = p

                max_p = -1
                p_label = None
                for label, p in pred_label_dict.items():
                    if p > max_p:
                        p_label = label
                        max_p = p
                pred[j] = p_label
            return pred



    def generateLabelDict(self, y):
        label_dict = {}
        for label in y:
            if label in label_dict:
                label_dict[label] += 1
            else:
                label_dict[label] = 1
        return label_dict


    def calc_mean_var(self, X):
        u = np.mean(X)
        v = np.var(X, ddof=1)
        return u, v