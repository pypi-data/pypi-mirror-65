"""
The datasets module provides access to some example alloy datasets
"""

import pandas as pd

from os import path

HERE = path.dirname(__file__)
DATA_PATH = path.join(HERE, 'data')


def Al_maxUTS_MIF():
    """A selection of Al-alloys for predicting UTS.

    :return: dataset as pandas dataframe

    Usage:
    >>> alloys = Al_maxUTS_MIF()
    >>> len(alloys)
    167
    """
    return pd.read_csv(path.join(DATA_PATH, 'Al_maxUTS_MIF.csv'), index_col=0)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
