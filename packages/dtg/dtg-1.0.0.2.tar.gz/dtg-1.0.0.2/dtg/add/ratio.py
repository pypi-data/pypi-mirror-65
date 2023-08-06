import numpy as np


def r(x, p):
    if hasattr(p, '__iter__'):
        return np.array([r(x, i) for i in p])

    res = np.power(x, p)
    return np.max(res)/np.sum(res)
