"""
Module unload.py
"""
import io

import src.elements.s3_parameters as s3p
import src.elements.service as sr


class Unload:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, bucket name, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__s3_resource = service.s3_resource
        self.__s3_client = service.s3_client

    def exc(self, key_name: str):
        """

        :param key_name: The S3 path of the data file, excluding the bucket name, including the file name..
        :return:
        """

        blob = self.__s3_client.get_object(Bucket=self.__s3_parameters.bucket_name, Key=key_name)
        buffer = io.StringIO(blob['Body'].read().decode('utf-8'))

        return buffer
