from abc import ABCMeta
import numpy as np


class Output(metaclass=ABCMeta):

    def __init__(self, b0, b1):
        self.b0 = b0
        self.b1 = b1

    def score(self, x, y, threshold=0.95):
        good = 0
        allowed = [list, np.ndarray]

        if type(x) in allowed and type(y) in allowed:
            x = np.array(x)
            y = np.array(y)

            if x.shape == y.shape:

                result = self.predict(x)
                min_answers = np.multiply(y, threshold)
                max_answers = np.multiply(y, 1 - threshold) + y

                for prediction, answer in zip(result, zip(min_answers, max_answers)):
                    if answer[1] >= prediction >= answer[0]:
                        good += 1

                accuracy = np.divide(good, x.shape[0])

            else:
                raise ValueError("Shape of x is not equal the shape of y.")

        else:
            raise TypeError(f"x is {type(x)} and y is {type(y)} where both should be {np.ndarray} or {list}")

        return accuracy

    def predict(self, x):
        if not isinstance(x, int):
            x = np.array(x)
            if len(x.shape) == 1:
                x.shape = (x.shape[0], 1)

            if x.shape[1] == np.array([self.b0]).shape[0]:
                result = np.multiply(x, self.b1) + self.b0

            else:
                raise ValueError("x shape is not correct")

        else:
            result = np.multiply(x, self.b1) + self.b0

        return result

