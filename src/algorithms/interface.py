"""
Module interface.py
"""
import logging

import dask.dataframe as ddf
import pandas as pd
import json

import src.algorithms.distributions
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

        self.__service = service
        self.__s3_parameters = s3_parameters

        self.__metadata = config.Config().metadata

        # The class instance for quantiles calculations, etc.
        self.__distributions = src.algorithms.distributions.Distributions()
        self.__meta = {0.1: float, 0.25: float, 0.5: float, 0.75: float, 0.9: float}
        self.__rename = {0.1: 'lower_decile', 0.25: 'lower_quartile', 0.5: 'median',
                         0.75: 'upper_quartile', 0.9: 'upper_decile'}

    def __quantiles(self, frame: ddf.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).apply(self.__distributions.quantiles, meta=self.__meta)
        content: pd.DataFrame = computations.compute(scheduler='processes')
        content.reset_index(drop=False, inplace=True)

        return content

    @staticmethod
    def __extrema(frame: ddf.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).agg(minimum=('measure', min), maximum=('measure', max))
        content: pd.DataFrame = computations.compute(scheduler='processes')
        content.reset_index(drop=False, inplace=True)

        return content

    def exc(self, branches: list[str], references: pd.DataFrame):
        """

        :param branches:
        :param references:
        :return:
        """

        structure = src.algorithms.structure.Structure(references=references)
        persist = src.algorithms.persist.Persist()
        upload = src.s3.upload.Upload(service=self.__service, bucket_name=self.__s3_parameters.external,
                                      metadata=self.__metadata)

        for branch in branches:

            # A collection of a device's timeseries data; retrieved in parallel
            frame: ddf.DataFrame = ddf.read_csv(branch)
            src.algorithms.numerics.Numerics(frame=frame.compute(scheduler="processes")).exc()

            # Calculations
            quantiles: pd.DataFrame = self.__quantiles(frame=frame)
            extrema: pd.DataFrame = self.__extrema(frame=frame)

            # Merge
            data: pd.DataFrame = quantiles.copy().merge(extrema.copy(), on=['sequence_id', 'date'], how='inner')
            data.rename(columns=self.__rename, inplace=True)

            # Structure
            nodes: dict = structure.exc(data=data)

            # Name
            dictionary: dict = nodes['attributes']
            name: str = f"pollutant_{dictionary['pollutant_id']}_station_{dictionary['station_id']}.json"

            # Upload
            # upload.bytes(buffer=json.dumps(nodes).encode('utf-8'),
            #              key_name=f'{self.__s3_parameters.path_external_quantiles}{name}')

            # Persist
            # persist.exc(nodes=nodes, name=name)
