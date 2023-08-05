import numpy as np
import time
import matplotlib.pyplot as plt




def count_time(func):
    def call_fun(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        end = time.time()
        print('fit complete -> time cost: %fs' % (end - start))
        return f
    return call_fun




class BaseModel(object):
    def __init__(self, n_iter=None, *args, **kwargs):
        self.n_iter = n_iter
        self.iteration = 0
        self.bar_nums = 30
        self.trained_sign = '='
        self.untrained_sign = '-'
        self.verbose = kwargs.pop('verbose', 0)


    @count_time
    def fit(self, *args):
        pass


    def predict(self, X, is_train, *args):
        raise NotImplementedError


    def backward(self, *args):
        raise NotImplementedError


    def step(self, *args):
        pass


    def get_acc(self, y, y_hat, reduction='mean'):
        y = np.asarray(y).flatten()
        y_hat = np.asarray(y_hat).flatten()
        return np.mean(y == y_hat) if reduction == 'mean' else np.sum(y == y_hat)



    def score(self, X, y, use_batch=None,reduction='mean', *args, **kwargs):
        X = np.asarray(X)
        y = np.asarray(y)
        if y.ndim == 1:
            y = np.expand_dims(y, axis=1)
        if use_batch is None:
            pred = self.predict(X, is_train=False)
        else:
            pred = np.zeros_like(y)
            n_sample = X.shape[0]
            s = 0
            e = min(s + use_batch, n_sample)
            while e < n_sample:
                pred[s: e] = self.predict(X[s: e], is_train=False)
                s = e
                e = min(s + use_batch, n_sample)

        acc = self.get_acc(y, pred, reduction)
        print('accuracy on test data is ', acc)
        return acc


    def train_verbose(self, acc=None, loss=None, iter_time=None, **kwargs):
        if self.verbose == 0:
            pass
        elif self.verbose == 1:
            print('iter {}, acc: {}, loss: {}'.format (self.iteration, acc, loss))
        elif self.verbose == 2:
            bar = self.process_bar(self.iteration, self.n_iter)
            eta_time = (self.n_iter - self.iteration) * iter_time
            formated_eta_time = self.format_time(eta_time)
            print('\riter {} {} -ETA {} acc: {}, loss: {}'.format(self.iteration, bar, formated_eta_time, acc, loss), flush=True, end='')


    def plot(self, *args):
        raise NotImplementedError


    def process_bar(self, cur_iter, max_iter):
        if max_iter == -1:
            max_iter = cur_iter
        finished = int(cur_iter * self.bar_nums / max_iter)
        bar = '[' + self.trained_sign * finished + '>' + self.untrained_sign * (self.bar_nums - finished - 1) + ']'
        return bar


    def format_time(self, second_time):
        if second_time < 1:
            ms = second_time * 1000
            if ms < 1:
                us = second_time * 1000
                return '%dus' % us
            else:
                return '%dms' % ms
        second_time = round(second_time)
        if second_time > 3600:
            # hours
            h = second_time // 3600
            second_time = second_time % 3600
            # minutes
            m = second_time // 60
            second_time = second_time % 60
            return '%dh%dm%ds' % (h, m, second_time)
        elif second_time > 60:
            m = second_time // 60
            second_time = second_time % 60
            return '%dm%ds' % (m, second_time)
        else:
            return '%ds' % second_time

