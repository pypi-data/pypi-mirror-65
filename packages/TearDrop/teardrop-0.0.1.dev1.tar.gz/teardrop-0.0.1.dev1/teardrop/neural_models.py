from teardrop.core.training import Model


class Sequential(Model):
    # TODO: Implement C++ version of NeuralNetwork class for better performance.

    """Neural model used for performing various deep learning tasks.


    NeuralNetwork class for performing deep learning. To perform deep learning you have to add layers (min. 1)
    to the network using ``.add()`` function and passing proper layer type.

    Example
    ---------
    Example importing and usage of the model.

    >>> import teardrop.neural_models.Sequential as Net
    >>> from teardrop.layers.core import Dense
    >>> model = Net()
    >>> model.add(Dense(2, activation='sigmoid', input_shape=2))
    >>> model.fit(x, y, n_epochs=5000)


    Functions
    ----------
    fit
        Used for performing model fitting on specified data.

    predict
        Used for making model predict after fitting based on passed data.

    add
        Function used to add layers to the network required for deep learning.

    initialize
        Function used for initializing weights and biases for network.
        You don't have to use it as weights and biases are automatically initialized during fitting!

    history
        Returns the history of losses after fitting.
    """

    def __init__(self, loss='mse', optimizer='sgd', show_progress=False):
        super().__init__(loss, optimizer, show_progress)

    def fit(self, x, y, learning_rate=0.01, n_epochs=5000, batch_size=1):

        """
        Network class function used for fitting data into the model allowing it
        to predict values.

        Parameters
        -----------
        x: array-like
            Data used for model fitting.

        y: array-like
            Correct predictions for the model to perform back propagation.

        learning_rate: float or int, optional
            Learning rate deciding how big the gradient step is.

        n_epochs: int, optional
            Number of times network will be trained on `x` data.

        batch_size: int, optional
            Number of data samples in one batch.

        Returns
        --------
        None
        """

        super().fit(x, y, learning_rate, n_epochs, batch_size)

    def predict(self, x):

        """
        Network class function used to make predicts based on the value passed
        in `x` argument.

        Parameters
        -----------
        x: array-like
            Matrix containing data for predicting.

        Returns
        --------
        prediction: array-like or float
            Prediction made by model on `x` data.
        """

        output = super().predict(x)
        return output

    def add(self, layer):

        """Network class function used for adding layers to the network.

        NeuralNetwork class function used for adding next layers to the network. Without layers network
        cannot perform fitting and predicting. For

        Parameters
        -----------
        layer
            Layer added to the network.

        Returns
        --------
        None

        See also
        ---------
        teardrop.layers
        """

        super().add(layer)

    def initialize(self, x):

        """
        Function which initializes the weights and biases for the network.
        !Initializing is not required as it's automatically done before fitting!

        Parameters
        -----------
        x: array-like
            Data matrix which's shape is used for initializing weights.

        Returns
        --------
        None
        """

        super().initialize(x)

    def history(self):

        """
        Function which is used to get the loss history to create various graphs.

        Returns
        --------
        self.loss_history: list
            List containing los for every epoch after fitting.
        """

        return self.loss_history

    def evaluate(self, x, y, threshold=0.9, type='accuracy'):

        """

        Parameters
        -----------
        x: array-like
            Data matrix used for performing forward propagation and evaluating.

        y: array-like
            Data matrix containing correct predictions for the network to check
            if predictions are correct.

        threshold: float or int
            The threshold which model's prediction has to pass to be considered good.

        type: str
            Type of the evaluation which model will use to evaluate.
            These types are available:
                * accuracy
        """

        result = super().evaluate(x, y, threshold, type)

        return result


class RNN:

    def __init__(self):
        pass
