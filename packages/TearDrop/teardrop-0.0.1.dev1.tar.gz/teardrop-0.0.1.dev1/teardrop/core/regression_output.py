from teardrop.core._abstract_classes._base_classes._base_linear_output import Output


class RegressionResults(Output):

    def __init__(self, b0, b1):
        super().__init__(b0, b1)

    def score(self, x, y, threshold=0.95):

        """
        Parameters
        -----------
        x: array-like
            The point in x-axis used to predict the point in y-axis.

        y: array-like
            The correct point in y-axis which has to be predicted by the model.

        threshold: float/int
            The threshold which model's prediction has to fit to be called correct.

        Returns
        --------
        accuracy: float/int
            The accuracy of the model.
        """

        accuracy = super().score(x, y, threshold)
        return accuracy

    def predict(self, x):

        """
        Parameters
        ------------
        x: array-like/int/float
            Point in x-axis for which RegressionOutput class will predict point in y-axis.

        Returns
        ---------
        result: array-like/int/float
            Point in y-axis for which x was specified.
        """

        result = super().predict(x)
        return result
