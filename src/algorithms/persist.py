import logging

import numpy as np
import pandas as pd


class Persist:

    def __init__(self, references: pd.DataFrame):
        """
        Constructor
        """

        self.__references = references

        self.__fields = ['epochmilli', 'lower_decile', 'lower_quartile', 'median', 'upper_quartile', 'upper_decile',
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

    def __attributes(self, sequence_id):

        attributes: pd.DataFrame = self.__references.copy().loc[self.__references['sequence_id'] == sequence_id, :]

        return attributes.to_dict(orient='records')

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        frame: pd.DataFrame = self.__epoch(blob=data.copy())
        dictionaries = frame.to_dict(orient='tight')

        # Attributes
        sequence_id: int = frame['sequence_id'].unique()[0]
        attributes = self.__attributes(sequence_id=sequence_id)


        logging.log(level=logging.INFO, msg=frame)
        logging.log(level=logging.INFO, msg=attributes)
        logging.log(level=logging.INFO, msg=dictionaries['columns'])
