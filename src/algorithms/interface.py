"""
Module interface.py
"""
import logging

import dask
import dask.dataframe as ddf
import pandas as pd

import config
import src.algorithms.numerics
import src.algorithms.persist
import src.algorithms.structure
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.upload


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
        self.__metadata: dict[str, str] = config.Config().metadata

    @dask.delayed
    def __data(self, branch: str) -> pd.DataFrame:
        """

        :param branch:
        :return:
        """

        # A collection of a device's timeseries data; retrieved in parallel
        frame: ddf.DataFrame = ddf.read_csv(branch)
        data: pd.DataFrame = src.algorithms.numerics.Numerics(frame=frame.compute()).exc()

        return data

    @dask.delayed
    def __name(self, nodes: dict) -> str:
        """

        :param nodes:
        :return:
        """

        # Name
        dictionary: dict = nodes['attributes']
        name: str = f"pollutant_{dictionary['pollutant_id']}_station_{dictionary['station_id']}.json"

        return name

    def exc(self, branches: list[str], references: pd.DataFrame):
        """

        :param branches: The Amazon S3 bucket branches, each branch is associated 
                         with a single telemetric device station/pollutant
        :param references: The inventory of station/telemetric device/pollutant metadata.
        :return:
        """

        __structure = dask.delayed(src.algorithms.structure.Structure(references=references).exc)
        __upload = dask.delayed(src.s3.upload.Upload(
            service=self.__service, bucket_name=self.__s3_parameters.external,
            metadata=self.__metadata).bytes)
        __persist = dask.delayed(src.algorithms.persist.Persist().exc)


        computations = []
        for branch in branches:

            data: pd.DataFrame = self.__data(branch=branch)
            nodes: dict = __structure(data=data)
            name: str = self.__name(nodes=nodes)
            persisted = __persist(nodes=nodes, name=name)

            computations.append(persisted)

        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info(messages)
