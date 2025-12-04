"""
Module setup.py
"""

import config
import src.functions.directories
import src.s3.bucket
import src.s3.objects


class Setup:
    """
    Notes
    -----

    Prepares local and cloud depositories.    
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        # Configurations
        self.__configurations = config.Config()

    def __local(self) -> None:
        """
        
        :return:
            None
        """

        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__configurations.warehouse)
        directories.create(path=self.__configurations.storage)

    def exc(self) -> None:
        """
        
        :return:
            None
        """

        self.__local()
