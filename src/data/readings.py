import logging
import os

import dask.dataframe as ddf
import numpy as np

import src.elements.s3_parameters as s3p


class Readings:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

    def exc(self, s3_keys: list):
        """

        :param s3_keys:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        nodes = [f's3://{self.__s3_parameters.bucket_name}/{path}/*.csv' for path in paths]

        for node in nodes:
            frame = ddf.read_csv(urlpath=node)
            details = frame.compute(scheduler='processes')
            logging.log(level=logging.INFO, msg=details)
