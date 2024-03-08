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

    def __quantiles(self) -> cudf.DataFrame:
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
        
        calc.reset_index(drop=False, inplace=True, col_level=1, 
                         level=['sequence_id', 'date'], col_fill='indices')

        return calc

    def __extrema(self) -> cudf.DataFrame:
        """
        
        :return
        """

        calc: cudf.DataFrame = self.__data[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(['min', 'max'])

        calc.reset_index(drop=False, inplace=True, col_level=1,
                         level=['sequence_id', 'date'], col_fill='indices')

        return calc
    
    def __epoch(self, x: pd.Series) -> np.ndarray:
        """

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

        left: cudf.DataFrame = self.__quantiles()
        logging.log(level=logging.INFO, msg=left)
        
        right:cudf.DataFrame = self.__extrema()
        logging.log(level=logging.INFO, msg=right)

        calculations = left.copy().merge(
            right.copy(), on=[('indices', 'sequence_id'), ('indices', 'date')], how='inner')
        logging.log(level=logging.INFO, msg=calculations)

        # Continue developing ...
        # ... set_axis()  & list(x.columns.get_level_values(1))
        x = calculations.to_pandas()
        y = x.set_axis(labels=x.columns.get_level_values(level=1), axis=1)
        y.loc[:, 'epochmilli'] = self.__epoch(x=y['date'])
        logging.log(level=logging.INFO, msg=y)

        return y
