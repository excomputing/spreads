"""
Module numerics.py
"""
import logging
import cudf
import pandas as pd
import numpy as np

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


    def __quantiles(self) -> cudf.DataFrame:
        """
        Determines the daily quantiles of a series.  Unfortunately, groupby.quantile(q=np.array(...)) is still
        under development; re-write this function when it is available.
        
        :return:
            A CUDF data frame of quantiles
        """

        # The quantiles equations
        lower_decile = lambda x: x.quantile(0.1); lower_decile.__name__ = 'lower_decile'
        lower_quartile = lambda x: x.quantile(0.25); lower_quartile.__name__ = 'lower_quartile'
        median = lambda x: x.quantile(0.5); median.__name__ = 'median'
        upper_quartile = lambda x: x.quantile(0.75); upper_quartile.__name__ = 'upper_quartile'
        upper_decile = lambda x: x.quantile(0.9); upper_decile.__name__ = 'upper_decile'

        # Calculating per sequence date
        blob: cudf.DataFrame = self.__data.copy()[['sequence_id', 'date', 'measure']]
        calc: cudf.DataFrame = blob.groupby(by=['sequence_id', 'date']).agg(
            [lower_decile, lower_quartile, median, upper_quartile, upper_decile])

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

    def __epoch(self, x: pd.Series) -> np.ndarray:
        """
        Adding an epoch field; milliseconds seconds since 1 January 1970.

        :param blob:
        :return:
        """

        nanoseconds: pd.Series[int] = pd.to_datetime(x, format='%Y-%m-%d').astype(np.int64)
        milliseconds: pd.Series[int] = (nanoseconds / (10 ** 6)).astype(np.longlong)

        return milliseconds.array

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
        numbers.loc[:, 'epochmilli'] = self.__epoch(x=numbers['date'])
        logging.log(level=logging.INFO, msg=numbers)

        return numbers
