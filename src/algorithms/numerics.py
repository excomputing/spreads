"""
Module numerics.py
"""

import cudf
import numpy as np
import pandas as pd

import src.algorithms.points


class Numerics:
    """
    Notes
    -----

    Calculating quantiles & extrema via graphics processing units
    """

    def __init__(self, frame: pd.DataFrame) -> None:
        """
        
        :param frame: A telemetric device's time series.
        """

        self.__data: cudf.DataFrame = cudf.from_pandas(frame)

        self.__points = src.algorithms.points.Points()


    def __quantiles(self) -> cudf.DataFrame:
        """
        Determines the daily quantiles of a series.  Unfortunately, groupby.quantile(q=np.array(...)) is still
        under development; re-write this function when it is available.
        
        :return:
            A CUDF data frame of quantiles
        """

        # Calculating per sequence date
        blob: cudf.DataFrame = self.__data.copy()[['sequence_id', 'date', 'measure']]
        calc: cudf.DataFrame = blob.groupby(by=['sequence_id', 'date']).agg(
            [self.__points.lower_decile, self.__points.lower_quartile, self.__points.median,
             self.__points.upper_quartile, self.__points.upper_decile])

        calc.reset_index(drop=False, inplace=True, col_level=1,
                         level=['sequence_id', 'date'], col_fill='indices')

        return calc

    def __extrema(self) -> cudf.DataFrame:
        """
        Determines each day's minimum & maximum measurements, per sequence.
        
        :return:
            A CUDF data frame of extrema
        """

        calc: cudf.DataFrame = self.__data[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(['min', 'max'])

        calc.reset_index(drop=False, inplace=True, col_level=1,
                         level=['sequence_id', 'date'], col_fill='indices')

        return calc

    @staticmethod
    def __epoch(values: pd.Series) -> np.ndarray:
        """
        Adding an epoch field; milliseconds seconds since 1 January 1970.

        :param values:
        :return:
        """

        nanoseconds: pd.Series= pd.to_datetime(values, format='%Y-%m-%d').astype(np.int64)
        milliseconds: pd.Series = (nanoseconds / (10 ** 6)).astype(np.longlong)

        return milliseconds.to_numpy()

    def exc(self) -> pd.DataFrame:
        """
        
        :return
        """

        # Quantiles & Extrema
        quantiles: cudf.DataFrame = self.__quantiles()
        extrema:cudf.DataFrame = self.__extrema()
        calculations = quantiles.copy().merge(
            extrema.copy(), on=[('indices', 'sequence_id'), ('indices', 'date')], how='inner')

        # Transform to a pandas data frame
        values = calculations.to_pandas()
        numbers = values.set_axis(labels=values.columns.get_level_values(level=1), axis=1)

        # Rename fields
        numbers.rename(columns={'min': 'minimum', 'max': 'maximum'}, inplace=True)

        # Append an epoch field
        numbers.loc[:, 'epochmilli'] = self.__epoch(values=numbers['date'])

        return numbers
