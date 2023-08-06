import numpy as np
from teardrop.core._abstract_classes._abstract_optimizers import AbstractSGD


class SGD(AbstractSGD):

    def __init__(self):
        super().__init__()

    def update(self, gradient, lr):
        """
        Parameters
        -----------
        gradient: array-like
            The array with gradient already changed to update weights.

        lr: float/int
            The "length" of the step in updating weights.

        Returns
        --------
        update_size: array-like
            The gradient required for back propagation.
        """

        change = super().update(gradient, lr)
        return change
