import numpy as np


def boot(entity, x, alp, beta, num, k):
    if hasattr(k, '__iter__'):
        return np.array([boot(entity, x, alp, beta, num, i) for i in k])

    try:
        k1 = int(k * (x.size ** ((1 - beta) * alp)))
        n1 = int(x.size ** beta)
        if k1 + 1 > n1:
            k1 = n1 - 1

        ga = []
        for _ in np.arange(num):
            sub_x = np.array([x[i] for i in np.random.choice(np.arange(0, x.size), n1, replace=True)])
            sub_x.sort()
            ga.append(entity.estimate(sub_x, k1))

        ga = np.array(ga)
        real = entity.estimate(x, k)
        bias = (np.mean(ga[~np.isnan(ga)]) - real) ** 2
        vr = np.var(ga[~np.isnan(ga)])
        return vr + bias, real
    except Exception as error:
        print(error)
        return np.infty, 0
    except OverflowError as error:
        print(error)
        return np.infty, 0
