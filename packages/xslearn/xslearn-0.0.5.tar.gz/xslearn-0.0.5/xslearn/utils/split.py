import numpy as np




def train_test_split(X, y,**kwargs):
    X, y = np.asarray(X), np.asarray(y)
    assert len(X) != 0, "X can not be empty~"
    test_size = kwargs.pop('test_size', None)
    train_size = kwargs.pop('train_size', None)
    random_state = kwargs.pop('random_state', None)
    shuffle = kwargs.pop('shuffle', True)
    stratify = kwargs.pop('stratify', False)
    if kwargs:
        raise TypeError('unknwon parameters: ', str(kwargs))
    if test_size is None and train_size is None:
        test_size = 0.2
    elif train_size is not None and test_size is not None:
        assert train_size + test_size == 1, "train_size + test_size must be equal to 1"
    elif test_size is not None:
        assert 0. <= test_size < 1., 'test_size must be >= 0. and < 1.'
    elif train_size is not None:
        assert 0. < train_size <= 1., 'train_size must be > 0. and <= 1.'
        test_size = 1. - train_size

    if random_state is not None:
        np.random.seed(random_state)

    n_samples = len(X)
    n_index = list(range(n_samples))
    if shuffle:
        np.random.shuffle(n_index)
        X, y = X[n_index], y[n_index]

    train_nums = n_samples - round(n_samples * test_size)
    if stratify:
        # stratified sampling
        assert y is not None, 'make sure parameter y is not None when using stratified sampling!'
        train_X, test_X, train_y, test_y = [], [], [], []
    else:
        train_X, test_X, train_y, test_y = X[:train_nums], X[train_nums:], y[:train_nums], y[train_nums:]
    return train_X, test_X, train_y, test_y




def sampling2d(X, y, bootstrap, nums, axis=0, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)
    if axis == 0:
        m = len(X)
    else:
        m = len(X[0])
    if bootstrap:
        sample_idx = np.random.choice(m, nums)
    else:
        sample_idx = np.random.choice(m, nums, replace=False)
    if axis == 0:
        sampled_X = X[sample_idx, :]
        sampled_y = y[sample_idx]
        return sampled_X, sampled_y, sample_idx
    else:
        return sample_idx


