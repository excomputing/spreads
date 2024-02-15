import dask.dataframe as ddf
import config
import logging

import src.elements.s3_parameters as s3p


class Readings:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

        configurations = config.Config()
        self.__source = configurations.source

    def exc(self):
        """

        :return:
        """

        frame = ddf.read_csv(urlpath=self.__source)
        details = frame.compute(scheduler='processes')
        logging.log(level=logging.INFO, msg=details)
