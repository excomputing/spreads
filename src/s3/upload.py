"""
Module upload.py
"""

import boto3
import botocore.exceptions

import src.elements.service as sr


class Upload:
    """
    Cf. the Action sections of
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/object/index.html#S3.Object

        The second is derivable from the first via
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/Object.html
    """

    def __init__(self, service: sr.Service, bucket_name: str, metadata: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of the Amazon S3 bucket that a data set is being delivered to.
        :param metadata: The metadata of the data
        """

        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__bucket_name: str = bucket_name
        self.__metadata: dict = metadata

    def bytes(self, buffer: bytes, key_name: str) -> bool:
        """

        :param buffer: The data that will be delivered to Amazon S3
        :param key_name: The key name of the data -> {}/{}/{}.extension
        :return:
        """

        # A bucket object
        bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

        try:
            bucket.put_object(
                Body=buffer,
                Key=key_name,
                Metadata=self.__metadata)
            return True or False
        except botocore.exceptions.ClientError as err:
            raise err from err
