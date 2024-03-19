"""
Module interface.py
"""

import json
import dask.dataframe as ddf
import pandas as pd

import src.algorithms.numerics
import src.algorithms.persist
import src.algorithms.structure
import src.elements.service as sr
import src.elements.s3_parameters as s3p
import src.s3.upload

import config


class Interface:
    """
    Evaluates daily distributions of measures
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # The metadata of the resulting JSON files.
        metadata: dict[str, str] = config.Config().metadata
        self.__upload = src.s3.upload.Upload(service=self.__service, bucket_name=self.__s3_parameters.external,
                                             metadata=metadata)

        # Persist
        self.__persist = src.algorithms.persist.Persist()

    def exc(self, branches: list[str], references: pd.DataFrame):
        """

        :param branches: The Amazon S3 bucket branches, each branch is associated 
                         with a single telemetric device station/pollutant
        :param references: The inventory of station/telemetric device/pollutant metadata.
        :return:
        """

        structure = src.algorithms.structure.Structure(references=references)

        for branch in branches:

            # A collection of a device's timeseries data; retrieved in parallel
            frame: ddf.DataFrame = ddf.read_csv(branch)
            data: pd.DataFrame = src.algorithms.numerics.Numerics(frame=frame.compute(scheduler="processes")).exc()

            # Structure
            nodes: dict = structure.exc(data=data)

            # Name
            dictionary: dict = nodes['attributes']
            name: str = f"pollutant_{dictionary['pollutant_id']}_station_{dictionary['station_id']}.json"

            # Upload
            self.__upload.bytes(buffer=json.dumps(nodes).encode('utf-8'),
                         key_name=f'{self.__s3_parameters.path_external_quantiles}{name}')

            # Persist
            self.__persist.exc(nodes=nodes, name=name)
