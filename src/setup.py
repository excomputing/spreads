
import config

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.bucket
import src.s3.objects
import src.functions.directories

class Setup:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters) -> None:
        """
        
        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """
        
        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        self.__configurations = config.Config()

    def __local(self):
        
        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__configurations.storage)
        directories.create(path=self.__configurations.storage)

    def __cloud(self):

        # Preparing the externally facing Amazon S3 bucket & path
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint, 
                                      bucket_name=self.__s3_parameters.external)
        objects = src.s3.objects.Objects(service=self.__service, bucket_name=self.__s3_parameters.external)

        iterable = objects.filter(prefix=self.__s3_parameters.path_external_quantiles)

        if bucket.exists():
            iterable.delete()
        else:
            bucket.create()

    def exc(self):

        self.__local()
        self.__cloud()    
