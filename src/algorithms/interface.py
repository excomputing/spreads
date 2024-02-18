"""
Module interface.py
"""
import logging

import dask.dataframe as ddf
import pandas as pd

import src.algorithms.distributions
import src.algorithms.persist
import src.algorithms.structure


class Interface:
    """
    Evaluates daily distributions of measures
    """

    def __init__(self):
        """
        Constructor
        """

        # The class instance for quantiles calculations
        self.__distributions = src.algorithms.distributions.Distributions()

        # Quantiles settings
        self.__meta = {0.1: float, 0.25: float, 0.5: float, 0.75: float, 0.9: float}
        self.__rename = {0.1: 'lower_decile', 0.25: 'lower_quartile', 0.5: 'median',
                         0.75: 'upper_quartile', 0.9: 'upper_decile'}

    def __quantiles(self, frame: ddf.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).apply(self.__distributions.quantiles, meta=self.__meta)
        content: pd.DataFrame = computations.compute(scheduler='processes')
        content.reset_index(drop=False, inplace=True)

        return content

    @staticmethod
    def __extrema(frame: ddf.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(minimum=('measure', min), maximum=('measure', max))
        content: pd.DataFrame = computations.compute(scheduler='processes')
        content.reset_index(drop=False, inplace=True)

        return content

    def exc(self, nodes: list[str], references: pd.DataFrame):
        """

        :param nodes:
        :param references:
        :return:
        """

        structure = src.algorithms.structure.Structure(references=references)
        persist = src.algorithms.persist.Persist()

        for node in nodes:

            # A collection of a device's timeseries data; retrieved in parallel
            frame: ddf.DataFrame = ddf.read_csv(node)

            # Calculations
            quantiles = self.__quantiles(frame=frame)
            extrema = self.__extrema(frame=frame)

            # Merge
            data = quantiles.copy().merge(extrema.copy(), on=['sequence_id', 'date'], how='inner')
            data.rename(columns=self.__rename, inplace=True)

            # Structure
            nodes = structure.exc(data=data)

            # Persist
            persist.exc(nodes=nodes)
