from .base import *
from ..utils.toolkit import get_batch


class BaseLinearModel(BaseModel):
    def __init__(self, n_features, lr=0.1, n_iter=1000, shuffle=False, verbose=1, *args, **kwargs):
        super(BaseLinearModel, self).__init__(n_iter)
        self.n_iter = n_iter
        self.lr = lr
        self.shuffle = shuffle
        self.w = None
        self.b = None
        self.loss = []
        self.acc = []
        self.verbose = verbose
        self.initial_params(n_features)



    def initial_params(self, n_features):
        self.w = np.zeros((n_features, 1))
        self.b = np.zeros((1,))



    def step(self, dw, db):
        self.w = self.w - self.lr * dw
        self.b = self.b - self.lr * db

    @property
    def params(self):
        return (self.w, self.b)


    def summary(self):
        plt.figure()
        plt.title('training')
        plt.subplot(1, 2, 1)
        plt.plot(self.acc)
        plt.xlabel('iteration')
        plt.ylabel('acc')
        plt.subplot(1, 2, 2)
        plt.plot(self.loss)
        plt.xlabel('iteration')
        plt.ylabel('loss')
        plt.show()






class Perceptron(BaseLinearModel):
    def __init__(self, n_features, lr=0.1, n_iter=1000, shuffle=False, verbose=1):
        super(Perceptron, self).__init__(n_features, lr, n_iter, shuffle, verbose)


    @count_time
    def fit(self, X, y, batch_size=None):
        X, y = np.asarray(X), np.asarray(y)
        wrong_nums = 0
        while self.iteration < self.n_iter:
            batches = get_batch(X, y, 1, self.shuffle)
            for x, y_ in batches:
                t1 = time.time()
                y_hat = self.predict(x)
                loss = self.get_loss(y_, y_hat)
                self.loss.append(loss)
                if y_ * y_hat <= 0:
                    wrong_nums += 1
                    dw, db = self.backward(x, y_)
                    self.step(-dw, -db)
                t2 = time.time()
                iter_time = t2 - t1
                self.iteration += 1
                acc = self.get_acc(y_, self.predict(x, is_train=False))
                self.acc.append(acc)
                self.train_verbose(acc, loss, iter_time)
                if self.iteration >= self.n_iter:
                    break
            if wrong_nums == 0:
                break
        if self.verbose == 2:
            print()


    def get_loss(self, y, y_hat):
        wrong_idx = y != y_hat
        loss = abs(np.sum(y[wrong_idx] * y_hat[wrong_idx]))
        return loss


    def backward(self, *args):
        x, y = args
        dw = y * x.T
        db = y
        return dw, db



    def predict(self, X, is_train=True, *args):
        if X.ndim == 1:
            X = np.expand_dims(X, axis=0)
        y_hat = np.dot(X, self.w) + self.b
        return y_hat if is_train else np.sign(y_hat)




class LogisticRegression(BaseLinearModel):
    def __init__(self, n_features, lr=0.1, n_iter=1000, shuffle=False, verbose=1):
        super(LogisticRegression, self).__init__(n_features, lr, n_iter, shuffle, verbose)


    @count_time
    def fit(self, X, y, batch_size=None):
        batches = get_batch(X, y, batch_size, self.shuffle)
        for x, y_ in batches:
            t1 = time.time()
            y_hat = self.predict(x)
            loss = self.get_loss(y_, y_hat)
            self.loss.append(loss)
            dw, db = self.backward(x, y_, y_hat)
            self.step(dw, db)
            t2 = time.time()
            iter_time = t2 - t1
            acc = self.get_acc(y_, self.predict(x, is_train=False))
            self.acc.append(acc)
            self.iteration += 1
            self.train_verbose(acc, loss, iter_time)
            if self.iteration >= self.n_iter:
                break
        if self.verbose == 2:
            print()


    def get_loss(self, y, y_hat):
        loss = np.mean(- y * np.log(y_hat) - (1 - y) * np.log(1 - y_hat))
        return loss



    def backward(self, *args):
        x, y_, y_hat = args
        m = x.shape[0]
        dw = x.T.dot(y_hat - y_) / m
        db = np.mean(y_hat - y_)
        return dw, db



    def predict(self, X, is_train=True, *args):
        if X.ndim == 1:
            X = np.expand_dims(X, axis=0)
        y_hat = np.dot(X, self.w) + self.b
        y_hat = self.sigmoid(y_hat)
        if not is_train:
            y_hat[y_hat > 0.5] = 1
            y_hat[y_hat <= 0.5] = 0
        return y_hat


    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
