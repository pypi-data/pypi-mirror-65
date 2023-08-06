import numpy as np
from teardrop.core._abstract_classes._base_classes._base_layer import Layer
from abc import ABCMeta
import copy
import teardrop.core.math.activations as math


class AbstractDenseLayer(Layer, metaclass=ABCMeta):

    def __init__(self, number_of_neurons, activation, input_shape=None):
        self.weights = []
        self.biases = []
        self.layer_input = None
        self.layer_output = None
        self.input_shape = input_shape

        if isinstance(number_of_neurons, int):
            self.neurons = number_of_neurons
        else:
            raise ValueError(f"Number of neurons in layer has to be int, not {type(number_of_neurons)}.")

        if activation == 'sigmoid':
            self.activation = math.Sigmoid()

        elif activation == 'relu':
            self.activation = math.Relu()

        else:
            raise TypeError(f"There is no activation function named {activation} or it hasn't been implemented yet.")

    def _forward(self, x):

        self.layer_input = x
        self.layer_output = np.dot(x, self.weights) + self.biases
        return self.activation.activate(self.layer_output)

    def _backward(self, last_derivative, lr, optimizer):

        w = copy.copy(self.weights)

        dfunction = np.multiply(last_derivative, self.activation.gradient(self.layer_output))
        d_w = np.multiply(np.dot(self.layer_input.T, dfunction), (1. / self.layer_input.shape[1]))
        d_b = np.divide(1., self.layer_input.shape[1]) * np.dot(np.ones((self.biases.shape[0], last_derivative.shape[0])),
                                                                dfunction)

        self.weights -= optimizer.update(d_w, lr)
        self.biases -= np.multiply(lr, d_b)

        return np.dot(dfunction, w.T)

    def _initialize(self, neurons):

        self.weights = np.random.rand(neurons, self.neurons) / 100  # dividing by 100 to make it more precise
        self.biases = np.random.rand(1, self.neurons) / 100


class AbsRNN(Layer, metaclass=ABCMeta):

    def __init__(self, cells, learning_rate):
        self.lr = learning_rate
        self.cells = cells
        self.weights = []
        self.weightsV = []
        self.biases = []
        self.outputs = []

    def _forward(self, x):
        num_inputs = len(x)

        cell_values = list()
        cell_values.append(np.zeros(self.cells))
        passed_hidden_states = []
        passed_hidden_states.append(np.zeros(self.cells))

        # we are creating just the model
        # the whole functional layer will be added soon

        for cell_num in range(self.cells):
            """
            PSEUDOKOD
            
            1. Liczymy hidden state dla pierwszej komórki za pomocą:
                input * weight + last_hidden * weightV
            2. Aktywujemy hidden state.
            3. Przekazujemy hidden state do następnej linii oraz komórki.
            4. Zwracamy cały zwrot linii.
            """

            hidden_state = math.Sigmoid(np.dot(x, self.weights) + np.dot(passed_hidden_states[cell_num], self.weightsV))
            passed_hidden_states.append(copy.deepcopy(hidden_state))
            self.outputs.append(copy.deepcopy(hidden_state))

        outputs = np.array(self.outputs)
        return outputs

    def _backward(self, last_derivative, lr, optimizer):

        next_layer_delta = np.zeros(self.cells)
        weights_update = np.zeros(self.weights)
        weightsV_update = np.zeros(self.weightsV)

        for cell_num in range(self.cells-1, -1, -1):
            """
            1. We calculate the gradient for 
            """

            weights_update += np.dot(last_derivative, self.outputs[cell_num]) * math.Sigmoid.gradient(self.outputs[cell_num])
            prev_cell = self.outputs[cell_num - 1]
            weightsV_update += np.dot(prev_cell, self.outputs[cell_num])

        self.weights -= optimizer.update(weights_update, lr)
        self.weightsV -= optimizer.update(weightsV_update, lr)

        """
        def backward(self, xs, hs, ps, targets):
            # backward pass: compute gradients going backwards
            dU, dW, dV = np.zeros_like(self.U), np.zeros_like(self.W), np.zeros_like(self.V)
            db, dc = np.zeros_like(self.b), np.zeros_like(self.c)
            dhnext = np.zeros_like(hs[0])
            for t in reversed(range(self.seq_length)):
                dy = np.copy(ps[t])
                # through softmax
                dy[targets[t]] -= 1  # backprop into y
                # calculate dV, dc
                dV += np.dot(dy, hs[t].T)
                dc += dc
                # dh includes gradient from two sides, next cell and current output
                dh = np.dot(self.V.T, dy) + dhnext  # backprop into h
                # backprop through tanh non-linearity
                dhrec = (1 - hs[t] * hs[t]) * dh  # dhrec is the term used in many equations
                db += dhrec
                # calculate dU and dW
                dU += np.dot(dhrec, xs[t].T)
                dW += np.dot(dhrec, hs[t - 1].T)
                # pass the gradient from next cell to the next iteration.
                dhnext = np.dot(self.W.T, dhrec)
            # clip to mitigate exploding gradients
            for dparam in [dU, dW, dV, db, dc]:
                np.clip(dparam, -5, 5, out=dparam)
            return dU, dW, dV, db, dc
        """

        return weights_update

    def initialize(self, cells):
        self.weights = np.random.rand(cells, self.cells) / 100
        self.biases = np.random.rand(1, self.cells) / 100
        self.weightsV = np.random.rand(self.cells, self.cells) / 100
