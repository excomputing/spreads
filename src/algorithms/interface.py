import logging
import os

import dask.dataframe as ddf
import numpy as np
import pandas as pd

import src.algorithms.distributions
import src.elements.s3_parameters as s3p


class Interface:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

        self.__distributions = src.algorithms.distributions.Distributions()

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

    @staticmethod
    def __epoch(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        data = blob.copy()
        nanoseconds = pd.to_datetime(data.copy()['date'], format='%Y-%m-%d').astype(np.int64)
        data.loc[:, 'epochmilli'] = (nanoseconds / (10 ** 6)).astype(np.longlong)

        return data

    def exc(self, s3_keys: list):
        """

        :param s3_keys:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        nodes = [f's3://{self.__s3_parameters.bucket_name}/{path}/*.csv' for path in paths]

        for node in nodes:

            # A collection of a device's timeseries data; retrieved in parallel
            frame: ddf.DataFrame = ddf.read_csv(node)

            # Calculations
            quantiles = self.__quantiles(frame=frame)
            extrema = self.__extrema(frame=frame)

            # Merge
            data = quantiles.copy().merge(extrema.copy(), on=['sequence_id', 'date'], how='inner')
            data.rename(columns=self.__rename, inplace=True)

            # Epoch
            data = self.__epoch(blob=data)

            logging.log(level=logging.INFO, msg=data.head())
