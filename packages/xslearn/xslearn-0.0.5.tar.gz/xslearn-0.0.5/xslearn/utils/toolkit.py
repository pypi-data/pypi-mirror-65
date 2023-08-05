import numpy as np


def get_shuffle_index(X):
    all_index = [i for i in range(X.shape[0])]
    np.random.shuffle(all_index)
    return all_index


def get_batch(X, y, batch_size=None, shuffle=True):
    X = np.array(X)
    y = np.array(y)
    if y.ndim == 1:
        y = np.expand_dims(y, axis=1)
    if batch_size is None:
        while True:
            yield X, y
    m = X.shape[0]
    sp = 0
    ep = min(sp + batch_size, m)
    while True:
        if sp == m:
            sp = 0
            ep = min(sp + batch_size, m)
        if shuffle and sp == 0:
            shuffle_index = get_shuffle_index(X)
            X = X[shuffle_index]
            y = y[shuffle_index]
        batch_x = X[sp: ep]
        batch_y = y[sp: ep]
        sp = ep
        ep = min(sp + batch_size, m)
        yield batch_x, batch_y



def mean_std_scale(X, mean=None, std=None, return_u_v=False):
    if mean is None:
        mean = np.mean(X, axis=0)
    if std is None:
        std = np.std(X, axis=0, ddof=1)
    X = (X - mean) / std
    if return_u_v:
        return X, mean, std
    else:
        return X


def min_max_scale(X):
    x_min = np.min(X, axis=0)
    x_max = np.max(X, axis=0)
    return (X - x_min) / (x_max - x_min)

