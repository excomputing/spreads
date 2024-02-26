"""
Module distributions.py
"""
import numpy as np
import dask.dataframe as ddf


class Distributions:
    """
    Notes
    -----
    Determines the quantiles of a series.
    """

    def __init__(self):
        """

        """

        self.__decimals = np.array([0.1, 0.25, 0.5, 0.75,0.9])

    def quantiles(self, blob: ddf.DataFrame):
        """

        :return:
        """

        return blob['measure'].quantile(q=self.__decimals)
