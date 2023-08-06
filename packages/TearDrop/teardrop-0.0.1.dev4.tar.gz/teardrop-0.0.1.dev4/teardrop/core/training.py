import numpy as np
from teardrop.core._abstract_classes._base_classes.network import Network
from teardrop.core._abstract_classes._base_classes._base_layer import Layer
from teardrop.preprocessing import batch_iterator
from teardrop.core.tools.progress_bar import pyprogress


class Model(Network):
    """
    TODO: Make Neural Network asynchronous.
    TODO: Add exceptions for Network to make sure passed arguments are correct.
    """

    def __init__(self, loss, optimizer, show_progress=False):
        super().__init__(loss, optimizer, show_progress)

    def fit(self, x, y, learning_rate=0.01, n_epochs=5000, batch_size=1):
        super().fit(x, y, learning_rate=learning_rate, n_epochs=n_epochs, batch_size=batch_size)

        self.initialize(x)  # initializing the weights in biases in all layers

        y = self.y_reshape(x, y)

        # TODO: Make sure y.shape is correct (create tests and check if it works correctly on many samples (crucial!))
        for epoch in range(n_epochs):
            epoch += 1
            num = 0

            for x_batch, y_batch in batch_iterator(x, y, batch_size=batch_size):
                output = x_batch

                for layer in self.layers:
                    output = layer._forward(output)

                num += len(x_batch)

                loss = self.loss.count_loss(output, y_batch)
                self.loss_history.append(loss)

                if self.show_progress:
                    pyprogress(
                        num,
                        len(x),
                        prefix=f'Epoch {epoch}/{n_epochs} {round(100 *(epoch/n_epochs))}%',
                        suffix=f'Loss: {loss}',
                        length=50,
                        fill='='
                    )

                last_derivative = self.loss.gradient(output, y_batch)

                for layer in reversed(self.layers):
                    last_derivative = layer._backward(last_derivative, learning_rate, self.optimizer)

    def predict(self, x):
        # TODO: Add tests for checking the passed data as x
        for layer in self.layers:
            x = layer._forward(x)
        return x

    def add(self, layer):

        if isinstance(layer, Layer):
            if not len(self.layers):
                if layer.input_shape is not None:
                    if type(layer.input_shape) == tuple:
                        self.input_shape = layer.input_shape[0]

                    elif type(layer.input_shape) == int:
                        self.input_shape = layer.input_shape

                    else:
                        raise ValueError(
                            f"Wrong data type specified. Expected int or tuple, got {type(layer.input_shape)}."
                        )

                else:
                    raise TypeError(
                        "First layer of the network requires input_shape to be specified."
                    )

            self.layers.append(layer)

        else:
            raise TypeError(f"Expected class {Layer}, got {type(layer)} instead.")

    def initialize(self, x):
        # TODO: Write tests for initialization
        previous_neurons = self.input_shape
        for layer in self.layers:
            layer._initialize(previous_neurons)
            previous_neurons = layer.neurons

    def history(self):
        # TODO: Make sure it's called after fitting.
        return self.loss_history

    def evaluate(self, x, y, threshold=0.9, type='accuracy'):
        # TODO: Add more evaluating types

        prediction = self.predict(x)
        output = np.where(prediction >= threshold, 1, 0)

        if type == 'accuracy':
            good = 0

            for predict, correct in zip(output, y):
                if predict == correct:
                    good += 1

            result = np.divide(good, y.size)

        else:
            raise TypeError(f"There is no evaluating type like {type} or it hasn't been implemented")

        return result

    # TODO: Add summary command
    """
    def summary(self):
        Summary command will send:
        layers':
            * input shapes,
            * activation functions,
            * weights and biases,
        --------------------------
            * network's output
            * network's loss function
    """

    def y_reshape(self, x, y):
        y = np.array(y)
        x = np.array(x)

        try:
            y = y.reshape((x.shape[0], self.layers[-1].neurons))
        except ValueError:
            raise ValueError(
                f"Wrong y shape. Couldn't reshape matrix with shape {y.shape} to {(x.shape[0], self.layers[-1].neurons)}"
            )

        return y