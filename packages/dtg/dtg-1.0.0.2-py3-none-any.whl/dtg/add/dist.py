import numpy as np


def dist_func(x):
    srt = np.sort(x)
    return np.array([np.mean(x < x_) for x_ in srt]), srt


def quantile(x, u):
    return np.mean(x < u)
