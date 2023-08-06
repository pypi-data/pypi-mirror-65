import numpy as np


def qq_plot(x):
    x_ = np.sort(x)
    q = np.array([x_[int(x.size*(1 - (k+1)/(x.size-1)))] for k in np.arange(x.size)])
    return x_[::-1], q
