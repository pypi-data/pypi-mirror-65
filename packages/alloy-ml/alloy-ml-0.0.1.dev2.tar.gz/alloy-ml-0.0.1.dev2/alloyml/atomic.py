"""
Module provides functionality for creating alloy
feature representations for alloy recipes by
considering them as descriptions of atom populations.

>>> prop_value('Al', 'Speed of sound')
5100.0
>>> prop_value('Cu', 'Speed of sound')
3570.0
"""

import pandas as pd
import datasets

from os import path
dirname = path.dirname(__file__)
tab_filename = path.join(dirname, 'atomic_features.csv')
table = pd.read_csv(tab_filename, index_col=0)
properties = table.columns
elements = table.index


def prop_value(el, prop):
    return table.loc[el, prop]


def base_metal(alloy):
    """
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[50]
    >>> base_metal(alloy)
    'Al'
    """
    return max(elements_in(alloy), key=alloy.get)


def elements_in(alloy):
    """
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> list(elements_in(alloy))
    ['Al', 'Cu', 'Mg', 'Mn', 'Pb']
    """
    return (key for key in alloy.keys() if key in elements and alloy[key] > 0.0)


class Mean:
    """

    For example:
    >>> mean_sos = Mean('Speed of sound')
    >>> mean_sos
    mean(Speed of sound)
    >>> alloys = datasets.Al_maxUTS_MIF() #pd.read_csv(path.join(dirname, '..', 'data', 'AAl_maxUTS_MIF.csv'), index_col=0)
    >>> alloy = alloys.iloc[24]
    >>> mean_sos(alloy)
    4991.988
    """

    def __init__(self, prop):
        self.prop = prop
        self.string = 'mean({})'.format(prop)

    def __call__(self, alloy):
        """
        :param alloy: data series with elements representing mixture coefficients of elements
            with names matching the chemical element names: 'H', 'He', 'Li', 'Be', etc.
        :return: mean value of property in atomic population described by alloy
        """
        s = sum(alloy[key] * prop_value(key, self.prop) for key in alloy.keys() if key in elements)
        return s / 100

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class StdDev:
    """

    For example:
    >>> std_sos = StdDev('Speed of sound')
    >>> std_sos
    std(Speed of sound)
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> std_sos(alloy)
    1272.5303415141127
    """

    def __init__(self, prop):
        self.prop = prop
        self.string = 'std({})'.format(prop)

    def __call__(self, alloy):
        """
        :param alloy: data series with elements representing mixture coefficients of elements
            with names matching the chemical element names: 'H', 'He', 'Li', 'Be', etc.
        :return: standard deviation value of property in atomic population described by alloy
        """
        s = sum(alloy[key] * prop_value(key, self.prop) for key in alloy.keys() if key in elements)
        m = s / 100
        d = sum(alloy[key] * (alloy[key]/100 * prop_value(key, self.prop) - m)**2
                for key in alloy.keys() if key in elements)
        return (d / 100)**0.5

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class FeatureMap:
    """
    Feature map that maps alloys into representation space of atomic
    population features.

    >>> feat_map = FeatureMap(['Speed of sound', 'Lattice constant'], feat_types=[Mean, StdDev])
    >>> feat_map
    AtomicFeatureMap(mean(Speed of sound), std(Speed of sound), mean(Lattice constant), std(Lattice constant))
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> a = alloys.iloc[24]
    >>> a.name
    '2030-T3510'
    >>> b = feat_map(a)
    >>> b.name
    '2030-T3510'
    >>> b.values
    array([4991.988     , 1272.53034151,  407.053685  ,  105.23568474])
    >>> alloys_trans = alloys.apply(feat_map, axis=1)
    >>> alloys_trans.columns
    Index(['mean(Speed of sound)', 'std(Speed of sound)', 'mean(Lattice constant)',
           'std(Lattice constant)'],
          dtype='object')
    """

    def __init__(self, props, feat_types=[Mean]):
        """
        :param props: iterable collection of atomic properties used for feature representation
        :param feat_types: parameters of property distribution to compute the final features
        """
        self.features = [ft(prop) for prop in props for ft in feat_types]
        self.index = pd.Index(str(f) for f in self.features)
        self.string = 'AtomicFeatureMap({})'.format(', '.join(map(str, self.features)))

    def __call__(self, alloy):
        return pd.Series((f(alloy) for f in self.features), index=self.index, name=alloy.name)

    def __repr__(self):
        return self.string


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
