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

        # Logging: If necessary, set force = True
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

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

    def __attributes(self, sequence_id) -> dict:

        attributes: pd.DataFrame = self.__references.copy().loc[
                                   self.__references['sequence_id'] == sequence_id, :]

        return attributes.to_dict(orient='records')[0]

    def __dictionaries(self, blob: pd.DataFrame) -> dict:

        frame = blob.copy()[self.__fields]

        return frame.to_dict(orient='tight')

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # Adding an epoch field; milliseconds seconds since ...
        frame: pd.DataFrame = self.__epoch(blob=data.copy())

        # The dictionaries of <frame>
        dictionaries = self.__dictionaries(blob=frame)

        # The attributes of the data encoded by <frame>
        sequence_id: int = frame['sequence_id'].unique()[0]
        attributes = self.__attributes(sequence_id=sequence_id)

        # Preview
        structure = {
            'attributes': attributes, 'columns': dictionaries['columns'],
            'data': dictionaries['data']
        }
        self.__logger.info(structure)
