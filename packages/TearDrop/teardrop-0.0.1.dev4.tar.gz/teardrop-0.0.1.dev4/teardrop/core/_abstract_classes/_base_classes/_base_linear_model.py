import numpy as np
from teardrop.data_tools import load_headbrain
from abc import ABCMeta


class Linear(metaclass=ABCMeta):

    def fit(self, x, y):
        pass
