from teardrop.core._abstract_classes._base_classes._base_layer import Layer
from teardrop.core._abstract_classes._abstract_layers import AbstractDenseLayer
import numpy as np
import copy


class Dense(AbstractDenseLayer):

    """
    A fully connected Dense layer in a basic Neural Network

    Functions
    -----------
    _forward: coroutine
        A function used to count sum of weighted inputs to perform forward propagation.

    _backward: coroutine
        A function used for performing back propagation.

    _initialize: coroutine
        A function initializing weights and biases for the layer.
    """

    def __init__(self, number_of_neurons, activation, input_shape=None):
        super().__init__(number_of_neurons, activation, input_shape)

    def _forward(self, x):

        """
        Parameters
        -----------
        x: array-like
            Matrix containing data used for model fitting.

        Returns
        --------
        result: array-like
            Matrix after summing all the weighted inputs and performing activation.
        """

        output = super()._forward(x)
        return output

    def _backward(self, last_derivative, lr, optimizer):

        """
        Parameters
        -----------
        last_derivative: array-like
            A matrix containing gradient from the last layer.

        lr: float/int
            Learning rate deciding how big the step of the gradient is.

        optimizer: str
            Optimizer used for optimizing weights and biases.

        Returns
        --------
        last_derivative: array-like
            The derivative passed to the next layer for back propagation.
        """

        last_gradient = super()._backward(last_derivative, lr, optimizer)
        return last_gradient

    def _initialize(self, neurons):

        """
        Parameters
        -----------
        neurons: int
            Number of neurons in layer used to initialize weights.

        Returns
        --------
        None
        """

        super()._initialize(neurons)


class RNN:
    # TODO: Create an RNN

    def __init__(self):
        raise NotImplementedError("RNNs coming soon...")
