"""
Module structure.py
"""

import pandas as pd


class Structure:
    """
    Notes
    -----
    Structures data sets in line with candle stick graph expectations.
    """

    def __init__(self, references: pd.DataFrame):
        """

        :param references: Each instance of the references data frame describes the characteristics of a unique sequence of
        telemetric data.
        """

        self.__references: pd.DataFrame = references

        # The data fields of interest for the spreads graphs
        self.__fields: list[str] = ['epochmilli', 'lower_decile', 'lower_quartile', 'median',
                                    'upper_quartile', 'upper_decile', 'minimum', 'maximum', 'date']

    def __attributes(self, sequence_id) -> dict:
        """

        :param sequence_id:
        :return:
        """

        attributes: pd.DataFrame = self.__references.copy().loc[
                                   self.__references['sequence_id'] == sequence_id, :]

        return attributes.to_dict(orient='records')[0]

    def __dictionaries(self, blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        frame = blob.copy()[self.__fields]

        return frame.to_dict(orient='tight')

    def exc(self, data: pd.DataFrame) -> dict:
        """

        :param data: The daily quantiles & extrema calculations vis-à-vis a telemetric device, i.e., a pollutant,
        at a specific location.
        :return:
        """

        # The dictionaries of <frame>
        dictionaries = self.__dictionaries(blob=data)

        # The attributes of the data encoded by <frame>
        sequence_id: int = data['sequence_id'].unique()[0]
        attributes = self.__attributes(sequence_id=sequence_id)

        # The required JSON structure
        nodes = {
            'attributes': attributes,
            'columns': dictionaries['columns'],
            'data': dictionaries['data']
        }

        return nodes
