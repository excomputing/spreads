"""
Module unload.py
"""
import io

import src.elements.service as sr


class Unload:
    """
    Unloads data from Amazon S3 (Simple Storage Service).
    """

    def __init__(self, service: sr.Service):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        """

        self.__s3_client = service.s3_client

    def exc(self, bucket_name: str, key_name: str):
        """

        :param bucket_name:
        :param key_name: The S3 path of the data file, excluding the bucket name, including the file name.
        :return:
        """

        blob = self.__s3_client.get_object(Bucket=bucket_name, Key=key_name)
        buffer = io.StringIO(blob['Body'].read().decode('utf-8'))

        return buffer
