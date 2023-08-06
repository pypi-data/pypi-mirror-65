import teardrop.core.math.loss_functions as math
from teardrop.optimizers import SGD
from abc import ABCMeta
import numpy as np


class Network(metaclass=ABCMeta):

    def __init__(self, loss='mse', optimizer='sgd', show_progress=False):
        self.layers = []
        self.loss_history = []
        self.batch_size = None
        self.optimizer = optimizer
        self.show_progress = show_progress
        self.numpy_array_x = False
        self.numpy_array_y = False
        self.input_shape = None

        if loss == 'mse':
            self.loss = math.MeanSquaredError()

        elif loss == 'cross-entropy':
            self.loss = math.CrossEntropy()

        else:
            raise TypeError(f"There is no loss like {loss} or it hasn't been implemented yet.")

        if optimizer == 'sgd':
            self.optimizer = SGD()

    def fit(self, x, y, learning_rate=0.01, n_epochs=5000, batch_size=1):

        self.batch_size = batch_size
        if not isinstance(learning_rate, float):
            raise ValueError(f"Expected type float, got {type(learning_rate)} instead.")

        if not isinstance(n_epochs, int):
            raise ValueError(f"Expected type int or float, got {type(n_epochs)} instead.")

        if isinstance(x, np.ndarray):

            if len(x.shape) == 1:
                x.shape = (x.shape[0], 1)

            if not x.shape[1] == self.input_shape:
                raise ValueError(
                    f"Error when checking input: first layer's input expected {self.input_shape}, got {(x.shape[1], )}"
                )

        if not len(self.layers):
            raise ValueError("Cannot perform model fitting because there are no layers.")

    def predict(self, x):
        raise NotImplementedError

    def add(self, layer):
        raise NotImplementedError

    def initialize(self, x):
        raise NotImplementedError



