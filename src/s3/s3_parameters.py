"""Module s3_parameters.py"""
import os

import src.elements.s3_parameters as s3p
import src.functions.secret
import src.functions.serial


class S3Parameters:
    """
    Class S3Parameters

    Description
    -----------

    This class reads-in the YAML file of this project's overarching Amazon S3 (Simple Storage Service)
    parameters settings.  Parameters such as region code, the names of the source & delivery buckets, etc.

    S3 Express One Zone, which has 4 overarching regions
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-Regions-and-Zones.html
    """

    def __init__(self):
        """
        Constructor
        """

        self.__uri = os.path.join(os.getcwd(), 'resources', 's3_parameters.yaml')
        self.__secret = src.functions.secret.Secret()

    def __get_dictionary(self) -> dict:
        """

        :return:
            A dictionary, or excerpt dictionary, of YAML file contents
        """

        blob = src.functions.serial.Serial().get_dictionary(uri=self.__uri)

        return blob['parameters']

    def __build_collection(self, dictionary: dict) -> s3p.S3Parameters:
        """

        :param dictionary:
        :return:
            A re-structured form of the parameters.
        """

        s3_parameters = s3p.S3Parameters(**dictionary)

        # Parsing variables
        region_name: str = self.__secret.exc(secret_id='RegionCodeDefault')
        s3_parameters: s3p.S3Parameters = s3_parameters._replace(
            location_constraint=region_name, region_name=region_name)

        return s3_parameters

    def exc(self) -> s3p.S3Parameters:
        """

        :return:
            The re-structured form of the parameters.
        """

        dictionary = self.__get_dictionary()

        return self.__build_collection(dictionary=dictionary)
