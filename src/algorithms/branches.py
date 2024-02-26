"""
Module branches.py
"""
import os

import numpy as np

import src.elements.service as sr
import src.elements.s3_parameters as s3p

import src.s3.keys


class Branches:
    """

    Notes
    -----
    Determines the distinct paths that host points data within an Amazon S3 bucket.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

    @staticmethod
    def __branches(s3_keys: list, bucket_name: str) -> list[str]:
        """

        :param s3_keys: Amazon S3 file names, which include prefixes.
        :param bucket_name: The name of an Amazon S3 bucket.
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        patterns = [f's3://{bucket_name}/{path}/*.csv' for path in paths]

        return patterns

    def exc(self) -> list[str]:
        """

        :return:
            A list of distinct paths that host points data within an Amazon S3 bucket.
        """

        # The list of keys, i.e., CSV files, that store telemetric data
        # The nodes, i.e., the distinct paths.
        bucket_name = self.__s3_parameters.internal

        keys = src.s3.keys.Keys(service=self.__service, bucket_name=bucket_name)
        s3_keys = keys.particular(prefix=self.__s3_parameters.path_internal_points)

        return self.__branches(s3_keys=s3_keys, bucket_name=bucket_name)
