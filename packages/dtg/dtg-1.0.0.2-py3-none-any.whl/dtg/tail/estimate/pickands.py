import numpy as np
import math as m

from dtg.tail.estimate.estimator import TailEstimator


class PickandEstimator(TailEstimator):
    @staticmethod
    def get_k(x):
        return np.arange(1, m.floor(x.size/4)-1)

    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([PickandEstimator.estimate(x, i) for i in k])
        if 4*(k+1) >= x.size:
            k = x.size//4 - 1
        if x[-2*k-1] - x[-4*k-3] == 0:
            return -10
        if (x[-k] - x[-2*k-1])/(x[-2*k-1] - x[-4*k-3]) <= 0:
            return -10
        return m.log((x[-k] - x[-2*k-1])/(x[-2*k-1] - x[-4*k-3]),2)
