import numpy as np
from scipy import stats


def gerador_dados_dinamicos(u0, W, V, sample_size = 1000):
    sample_size = sample_size + 1

    u = np.zeros(sample_size)
    y = np.zeros(sample_size)
    u[0] = u0
    
    for iteration in range(1, sample_size):
        u[iteration] = stats.norm.rvs(loc = u[iteration-1], scale = np.sqrt(W))
        y[iteration] = stats.norm.rvs(loc = u[iteration], scale = np.sqrt(V))

    return y[1:], u[1:]