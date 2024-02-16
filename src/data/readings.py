import logging
import os

import dask.dataframe as ddf
import numpy as np
import pandas as pd

import src.algorithms.distributions
import src.elements.s3_parameters as s3p


class Readings:

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

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).apply(self.__distributions.quantiles, meta=self.__meta)
        content: pd.DataFrame = computations.compute(scheduler='processes')

        content.reset_index(drop=False, inplace=True)

        return content

    def __extrema(self, frame: ddf.DataFrame) -> pd.DataFrame:

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(minimum= ('measure', min), maximum=('measure', max))
        content: pd.DataFrame = computations.compute(scheduler='processes')

        content.reset_index(drop=False, inplace=True)

        return content

    def __structure(self, quantiles_: pd.DataFrame, extrema_: pd.DataFrame):

        data = quantiles_.copy()
        data.rename(columns=self.__rename)

        nanoseconds = pd.to_datetime(data['date'], format='%Y-%m-%d').astype(np.int64)
        data.loc[:, 'epochmilli'] = (nanoseconds / (10 ** 6)).astype(np.longlong)

        logging.log(level=logging.INFO, msg=data.head())
        logging.log(level=logging.INFO, msg=extrema_.head())

    def exc(self, s3_keys: list):
        """

        :param s3_keys:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        nodes = [f's3://{self.__s3_parameters.bucket_name}/{path}/*.csv' for path in paths]

        for node in nodes:
            frame: ddf.DataFrame = ddf.read_csv(node)
            quantiles = self.__quantiles(frame=frame)
            extrema = self.__extrema(frame=frame)
            self.__structure(quantiles_=quantiles, extrema_=extrema)
