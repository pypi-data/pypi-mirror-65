import numpy as np
from teardrop.core._abstract_classes._base_classes._base_loss_function import Loss


def clip(x):  # used to squeeze the input into probability between 0 and 1
    return np.clip(x, 1e-15, 1 - 1e-15)


class AbstractMeanSquaredError(Loss):

    def count_loss(self, x, y):
        return np.sum(np.multiply(0.5, np.square(x - y)))

    def gradient(self, x, y):
        return np.multiply(2, x - y)


class AbstractCrossEntropy(Loss):

    def count_loss(self, x, y):
        return -(np.sum(np.multiply(clip(y), np.log(clip(x))) + np.multiply(1 - clip(y), np.log(1 - clip(x))))) / y.shape[0]

    def gradient(self, x, y):
        return -(np.divide(clip(y), clip(x)) - np.divide(1 - clip(y), 1 - clip(x)))
