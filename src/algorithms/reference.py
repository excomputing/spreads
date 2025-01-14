"""
Module reference.py
"""
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Reference:
    """

    Notes
    -----

    Each instance of the reference data frame describes the characteristics of a unique sequence of
    telemetric data.  The details include sequence identification code, the geographic coordinates of
    the telemetric device, the pollutant being measured, the unit of measure, etc.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Data reading and writing instance; for separated values.
        self.__streams = src.functions.streams.Streams()

    def __read(self, filename: str) -> pd.DataFrame:
        """

        :param filename: the name of the Amazon S3 (Simple Storage Service) file being read.
        :return:
        """

        uri = f's3://{self.__s3_parameters.internal}/{self.__s3_parameters.path_internal_references}{filename}'
        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.api(text=text)

    def exc(self) -> pd.DataFrame:
        """

        :return:
          data : DataFrame
            An integration of (a) substances descriptive data, (b) stations gazetteer data,
            and (c) telemetric devices registry
        """

        reference = self.__read(filename='reference.csv')

        return reference
