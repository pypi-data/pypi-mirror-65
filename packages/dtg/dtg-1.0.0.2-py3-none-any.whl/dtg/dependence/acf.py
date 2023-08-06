import numpy as np


def acf(x, h=None):
    if h is None:
        hs = np.arange(2, x.size-2)
        return acf(x, hs), hs

    if hasattr(h, '__iter__'):
        return np.array([acf(x, i) for i in h])

    mn = np.mean(x)
    return np.sum(np.multiply(x[:x.size - h] - mn, x[h:] - mn)) / np.sum(np.power(x - mn, 2))


def acf_inf(x, h=None):
    if h is None:
        hs = np.arange(2, x.size-2)
        return acf_inf(x, hs), hs

    if hasattr(h, '__iter__'):
        return np.array([acf_inf(x, i) for i in h])

    return np.sum(np.multiply(x[:x.size - h], x[h:])) / np.sum(np.power(x, 2))
