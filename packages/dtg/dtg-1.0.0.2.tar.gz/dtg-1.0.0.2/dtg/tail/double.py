import numpy as np
import math as mth

from dtg.tail.estimate import HillEstimator


def double_boot(x):
    x_ = HillEstimator.prepare(x)
    g_0 = HillEstimator.estimate(x_, int(2 * mth.sqrt(x.size)))
    r_1 = 0.25 * g_0 * (x.size ** 0.25)
    r_2 = (0.25 * g_0 * (x.size ** 0.25)) ** 0.7

    ks = HillEstimator.get_k(x)
    ga = HillEstimator.estimate(x_, ks)

    mx = np.array([np.max([mth.sqrt(i+1) * (ga[i] - ga[k]) for i in np.arange(1, k)]) for k in np.arange(2, ga.size)])
    k_1 = np.where(mx > r_1)[0]
    if k_1.size == 0:
        return None, None
    k_1 = k_1[0] + 1
    k_2 = np.where(mx > r_2)[0]
    if k_2.size == 0:
        return None, None
    k_2 = k_2[0] + 1

    k_op = int(mth.pow(k_2 / mth.pow(k_1, 0.7), 10 / 3) * mth.pow(2 * g_0, 1 / 3) / 3) - 1
    return HillEstimator.estimate(x_, k_op), k_op
