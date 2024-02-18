"""
Module persist.py
"""
import logging
import os.path

import numpy as np
import pandas as pd

import src.functions.objects
import config


class Persist:
    """

    This class exports the daily quantiles calculations of a telemetric device, i.e., of a pollutant, to a JSON file.  The
    JSON file includes a summary of the underlying raw data's characteristics.
    """

    def __init__(self, ):

        self.__storage = config.Config().storage
        self.__objects = src.functions.objects.Objects()

        # Logging: If necessary, set force = True
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __write(self, nodes: dict) -> str:

        dictionary = nodes['attributes']

        message = self.__objects.write(
            nodes=nodes,
            path=os.path.join(self.__storage, f"pollutant_{dictionary['pollutant_id']}_station_"
                                              f"{dictionary['station_id']}.json"))

        return message

    def exc(self, nodes: dict):

        message = self.__write(nodes=nodes)
        self.__logger.info(message)
