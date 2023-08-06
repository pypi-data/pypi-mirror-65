import teardrop.core._abstract_classes._abstract_loss_functions as loss


class MeanSquaredError(loss.AbstractMeanSquaredError):

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

        mse_loss = super().count_loss(x, y)
        return mse_loss

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

        gradient = super().gradient(x, y)
        return gradient


class CrossEntropy(loss.AbstractCrossEntropy):
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

        ce_loss = super().count_loss(x, y)
        return ce_loss

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

        gradient = super().gradient(x, y)
        return gradient
