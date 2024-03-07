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

        self.__data = cudf.from_pandas(frame)

        # The quantile points
        self.__decimals: np.ndarray[float] = np.array([0.1, 0.25, 0.5, 0.75, 0.9])

        # Dictionary
        self.__dictionary = {0.1: 'lower_decile', 0.25: 'lower_quartile', 0.5: 'median',
                             0.75: 'upper_quartile', 0.9: 'upper_decile'}

    def __quantiles(self):
        """
        Unfortunately groupby.quantile(q=np.array(...)) is not yet functioning
        
        :return
        """

        lower_decile = lambda x: x.quantile(0.1); lower_decile.__name__ = 'lower_decile'
        lower_quartile = lambda x: x.quantile(0.25); lower_quartile.__name__ = 'lower_quartile'
        median = lambda x: x.quantile(0.5); median.__name__ = 'median'
        upper_quartile = lambda x: x.quantile(0.75); upper_quartile.__name__ = 'upper_quartile'
        upper_decile = lambda x: x.quantile(0.9); upper_decile.__name__ = 'upper_decile'

        blob = self.__data.copy()[['sequence_id', 'date', 'measure']]
        
        calc = blob.groupby(by=['sequence_id', 'date']).agg(
            [lower_decile, lower_quartile, median, upper_quartile, upper_decile])
        
        calc.reset_index(drop=False, inplace=True, level=1)

        return calc

    def __extrema(self):
        """
        
        :return
        """

        calc: cudf.DataFrame = self.__data[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(['min', 'max'])

        return calc

    def exc(self):
        """
        
        :return
        """

        left = self.__quantiles()
        print(type(left))
        print(left)

        right:cudf.DataFrame = self.__extrema()
        logging.log(level=logging.INFO, msg=right)

        # calculations = left.copy().merge(right.copy(), on=['sequence_id', 'date'], how='inner')
        # logging.log(level=logging.INFO, msg=calculations)
