"""
The datasets module provides access to some example alloy datasets
"""

import pandas as pd

from os import path

HERE = path.dirname(__file__)
DATA_PATH = path.join(HERE, '..', 'data')


def Al_maxUTS_MIF():
    return pd.read_csv(path.join(DATA_PATH, 'Al_maxUTS_MIF.csv'), index_col=0)

