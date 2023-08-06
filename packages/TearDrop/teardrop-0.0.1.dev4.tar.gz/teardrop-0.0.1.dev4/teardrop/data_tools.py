import pandas as pd
import numpy as np
import os
import importlib.resources


def load_headbrain():
    path = os.path.join(os.path.dirname(__file__), r'datasets/headbrain.csv')
    dataframe = pd.read_csv(path)
    return dataframe


def load_dinos():
    path = os.path.join(os.path.dirname(__file__), r'datasets/dinos.csv')
    dataframe = pd.read_csv(path)
    return dataframe
