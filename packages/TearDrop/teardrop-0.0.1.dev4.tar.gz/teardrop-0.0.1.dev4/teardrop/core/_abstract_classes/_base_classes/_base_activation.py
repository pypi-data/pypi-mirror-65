from abc import ABCMeta


class ActivationFunction(metaclass=ABCMeta):

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
        pass

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
        pass
