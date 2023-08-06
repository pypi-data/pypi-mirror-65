from teardrop.core._abstract_classes._abstract_linear_models import LinearModel


class LinearRegression(LinearModel):

    def fit(self, x, y):

        """
        Parameters
        -----------
        x: array-like
            The array containing data about x-axis used for fitting.

        y: array-like
            The array containing data about y-axis used for fitting.

        Returns
        ---------
        reg: RegressionOutput object
            Object containing coefficients used for predicting and checking accuracy.

        See also
        ---------
        teardrop.core.basic_linear_model.RegressionOutput
        """

        reg = super().fit(x, y)
        return reg
