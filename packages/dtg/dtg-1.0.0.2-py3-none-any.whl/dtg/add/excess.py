import numpy as np


def e_n(x, u=None):
    if u is None:
        t = np.copy(x)
        t.sort()
        us = np.array([(t[i]+t[i+1])/2 for i in np.arange(t.size-1)])
        return np.array([e_n(x, i) for i in us])

    if hasattr(u, '__iter__'):
        return np.array([e_n(x, i) for i in u])

    res = x[x > u]
    if res.size == 0:
        return 0
    return np.sum(res-u)/res.size
