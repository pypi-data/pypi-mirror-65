from abc import ABCMeta


class BaseOptimizer(metaclass=ABCMeta):

    def __init__(self):
        self.weight_update = None

    def update(self, gradient, learning_rate):
        raise NotImplementedError
