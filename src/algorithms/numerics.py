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
        self.__decimals = np.array([0.1, 0.25, 0.5, 0.75,0.9])

    def __quantiles(self):
        """
        
        :return
        """

        calc: cudf.DataFrame = self.__data[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).quantile(q=self.__decimals)

        return calc

    def __extrema(self):
        """
        
        :return
        """

        calc: cudf.DataFrame = self.__data[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(minimum=('measure', min), maximum=('measure', max))

        return calc


    def exc(self):
        """
        
        :return
        """

        left: cudf.DataFrame = self.__quantiles()
        right:cudf.DataFrame = self.__extrema()
        calculations = left.copy().merge(right.copy(), on=['sequence_id', 'date'], how='inner')
        logging.log(level=logging.INFO, msg=calculations)
