import teardrop.core._abstract_classes._abstract_activation as activations


class Sigmoid(activations.AbstractSigmoid):
    def activate(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated: array-like/int/float
            Matrix after performing activation on it.
        """

        activated = super().activate(x)
        return activated

    def gradient(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().gradient(x)
        return next_gradient


class Relu(activations.AbstractRelu):
    def activate(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated: array-like/int/float
            Matrix after performing activation on it.
        """

        activated = super().activate(x)
        return activated

    def gradient(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().activate(x)
        return next_gradient


class Softmax(activations.AbstractSigmoid):

    def activate(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated: array-like/int/float
            Matrix after performing activation on it.
        """

        activated = super().activate(x)
        return activated

    def gradient(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().gradient(x)
        return next_gradient

