import numpy as np
from teardrop.core._abstract_classes._base_classes._base_optimizer import BaseOptimizer


class AbstractSGD(BaseOptimizer):

    def __init__(self):
        super().__init__()

    def update(self, gradient, learning_rate):
        return np.multiply(gradient, learning_rate)