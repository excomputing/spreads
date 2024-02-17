import logging

import numpy as np
import pandas as pd


class Persist:

    def __init__(self):
        """
        Constructor
        """

        self.__expectations = ['epochmilli', 'lower_decile', 'lower_quartile', 'median', 'upper_quartile', 'upper_decile',
                               'minimum', 'maximum', 'date']

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

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        frame = self.__epoch(blob=data.copy())

        logging.log(level=logging.INFO, msg=frame)
