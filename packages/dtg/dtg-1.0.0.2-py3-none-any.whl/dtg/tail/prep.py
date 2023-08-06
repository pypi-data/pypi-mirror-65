import numpy as np

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.estimate.moment import MomentEstimator
from dtg.tail.estimate.pickands import PickandEstimator
from dtg.tail.estimate.ratio import RatioEstimator
from dtg.tail.mse import boot


def boot_estimate(entity, x, alp, beta, num, speed=True):
    k = entity.get_k(x)
    x_ = entity.prepare(x)

    if speed:
        if len(k) == 0:
            return 0, 0

        count = 0
        mse, alpr = boot(entity, x_, alp, beta, num, k[0])
        k_opt = k[0]

        for k_ in k:
            mse_, alp_ = boot(entity, x_, alp, beta, num, k_)

            if mse_ < mse:
                mse = mse_
                alpr = alp_
                k_opt = k_
                count = 0
            else:
                count += 1

            if count == int(0.1 * k.size) or count == 100:
                break
        return alpr, k_opt

    k = entity.get_k(x)
    x_ = entity.prepare(x)
    res = boot(entity, x_, alp, beta, num, k)
    mses = np.array([res[i][0] for i in np.arange(k.size)])
    alps = np.array([res[i][1] for i in np.arange(k.size)])

    ar = np.argmin(mses)
    return alps[ar], k[ar]


def basic_tail(data):
    alp, k = boot_estimate(HillEstimator, data, 1 / 2, 2 / 3, 100, speed=False)
    print("hill", 1 / alp, k)

    alp, k = boot_estimate(RatioEstimator, data, 1 / 2, 2 / 3, 100, speed=False)
    print("ratio", 1 / alp, k)

    alp, k = boot_estimate(MomentEstimator, data, 1 / 2, 2 / 3, 100, speed=False)
    print("moment", 1 / alp, k)

    alp, k = boot_estimate(PickandEstimator, data, 1 / 2, 2 / 3, 100, speed=False)
    if alp != 0:
        print("pickands", 1 / alp, k)
    else:
        print("pickands", alp, k)
