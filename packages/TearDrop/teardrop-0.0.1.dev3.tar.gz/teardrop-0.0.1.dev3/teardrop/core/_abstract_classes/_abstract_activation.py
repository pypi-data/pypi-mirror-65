from ._base_classes._base_activation import ActivationFunction
import numpy as np


class AbstractSigmoid(ActivationFunction):

    def activate(self, x):
        return np.divide(1, 1 + np.exp(-x))

    def gradient(self, x):
        sig = self.activate(x)
        return np.multiply(sig, 1 - sig)


class AbstractRelu(ActivationFunction):

    def activate(self, x):
        return np.where(x > 0, x, 0)

    def gradient(self, x):
        return np.where(x > 0, 1, 0)


class AbstractSoftmax(ActivationFunction):
    """
    TODO: Add gradient for Softmax activation.
    """

    def activate(self, x):
        x -= np.max(x)
        exp = np.exp(x)
        return np.divide(exp, np.sum(exp))

    def gradient(self, x):
        pass
