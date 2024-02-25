"""
Module persist.py
"""
import logging
import os.path

import config
import src.functions.objects


class Persist:
    """
    Notes
    -----
    This class exports the daily quantiles calculations of a telemetric device, i.e., of a pollutant, to a JSON file.  The
    JSON file includes a summary of the underlying raw data's characteristics.
    """

    def __init__(self):
        """
        Constructor
        """

        # The local storage parent directory
        self.__storage = config.Config().storage

        # An instance for writing JSON files
        self.__objects = src.functions.objects.Objects()

        # Logging: If necessary, set force = True
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __local(self, nodes: dict, name: str) -> str:
        """

        :param nodes:
        :return:
        """

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__storage, name))

        return message

    def exc(self, nodes: dict, name: str):
        """

        :param nodes:
        :param name:
        :return:
        """

        message = self.__local(nodes=nodes, name=name)
        self.__logger.info(message)
