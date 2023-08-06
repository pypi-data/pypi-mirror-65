from abc import ABCMeta


class Loss(metaclass=ABCMeta):

    def count_loss(self, x, y):

        """
        Parameters
        -----------
        x: array-like/int/float
            The array of answers predicted by the network.
        y: array-like/int/float
            Correct answers for the network to predict.

        Returns
        --------
        loss: float/int
            The network's loss.
        """

        pass

    def gradient(self, x, y):
        """
        Parameters
        -----------
        x: array-like/int/float
            The array of answers predicted by the network.
        y: array-like/int/float
            Correct answers for the network to predict.

        Returns
        --------
        gradient: float/int
            Gradient used to perform back propagation.
        """
        pass
