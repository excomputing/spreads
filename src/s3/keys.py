import logging
import boto3
import botocore.exceptions

import src.elements.s3_parameters as s3p
import src.elements.service as sr


class Keys:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__s3_client = service.s3_client
        self.__bucket = self.__s3_resource.Bucket(name=self.__s3_parameters.bucket_name)

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger: logging.Logger = logging.getLogger(__name__)

    def particular(self, prefix: str) -> list:

        try:
            dictionaries = self.__s3_client.list_objects_v2(Bucket=self.__s3_parameters.bucket_name, Prefix=prefix)
        except self.__s3_client.exceptions.NoSuchKey as err:
            raise Exception(err) from err
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

        items = [dictionary['Key'] for dictionary in dictionaries['Contents']]

        return items

    def all(self) -> list:

        try:
            state: dict = self.__bucket.meta.client.head_bucket(Bucket=self.__bucket.name)
        except self.__bucket.meta.client.exceptions.NoSuchBucket as err:
            raise Exception(err) from err
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

        if state:
            items = [k.key for k in list(self.__bucket.objects.all())]
        else:
            items = []

        return items
