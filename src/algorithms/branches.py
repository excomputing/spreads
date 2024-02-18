import os

import numpy as np

import src.elements.service as sr
import src.elements.s3_parameters as s3p

import src.s3.keys


class Branches:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

    @staticmethod
    def __branches(s3_keys: list, bucket_name: str) -> list[str]:
        """

        :param s3_keys:
        :param bucket_name:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        patterns = [f's3://{bucket_name}/{path}/*.csv' for path in paths]

        return patterns

    def exc(self) -> list[str]:
        """

        :return:
        """

        # The list of keys, i.e., CSV files, that store telemetric data
        # The nodes, i.e., the distinct paths
        bucket_name = self.__s3_parameters.source_bucket_name

        keys = src.s3.keys.Keys(service=self.__service, bucket_name=bucket_name)
        s3_keys = keys.particular(prefix=self.__s3_parameters.source_path_)

        return self.__branches(s3_keys=s3_keys, bucket_name=bucket_name)
