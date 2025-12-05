"""
Module setup.py
"""

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.bucket
import src.s3.objects


class Cloud:
    """
    Notes
    -----

    Prepares local and cloud depositories.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters) -> None:
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

    def __cloud(self) -> None:
        """
        Preparing the externally facing Amazon S3 (Simple Storage Service) bucket

        :return:
            None
        """

        # If the target bucket exists, create an object of its content
        objects = src.s3.objects.Objects(service=self.__service, bucket_name=self.__s3_parameters.external)
        iterable = objects.filter(prefix=self.__s3_parameters.path_external_spreads)

        # Create a bucket object
        bucket = src.s3.bucket.Bucket(service=self.__service,
                                      location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__s3_parameters.external)

        # If the bucket exists, empty it, otherwise create it
        if bucket.exists():
            iterable.delete()
        else:
            bucket.create()

    def exc(self) -> None:
        """

        :return:
            None
        """

        self.__cloud()
