import numpy as np


def batch_iterator(x, y=None, batch_size=1):
    samples = x.shape[0]
    for i in np.arange(0, samples, batch_size):
        begin = i
        end = min(i + batch_size, samples)

        if y is not None:
            yield x[begin:end], y[begin:end]

        else:
            yield x[begin:end]