"""
Module main.py
"""
import logging
import os
import sys

import boto3
import pandas as pd


def main():
    """
    The focus is the daily quantile spreads per station.  Note, the data sets of each
    telemetric device station are stored within a distinct Amazon S3 bucket branch.

    Upcoming:
        * README.md Illustration

    :return:
    """

    # Logging
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    # Branches
    branches = src.algorithms.branches.Branches(service=service, s3_parameters=s3_parameters).exc()

    # References
    references: pd.DataFrame = src.algorithms.reference.Reference(s3_parameters=s3_parameters).exc()

    # Calculate quantiles
    src.algorithms.interface.Interface(service=service, s3_parameters=s3_parameters).exc(
        branches=branches, references=references)

    # Delete cache directories
    src.functions.cache.Cache().delete()


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Activate graphics processing units
    os.environ['CUDA_VISIBLE_DEVICES']='0'

    # Modules
    import src.algorithms.branches
    import src.algorithms.interface
    import src.algorithms.reference

    import src.elements.s3_parameters as s3p
    import src.elements.service as sr

    import src.functions.cache
    import src.functions.service
    import src.s3.s3_parameters
    import src.setup

    # S3 S3Parameters, Service Instance
    connector = boto3.session.Session()
    s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
    service: sr.Service = src.functions.service.Service(
        connector=connector, region_name=s3_parameters.region_name).exc()

    # Setting up
    src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

    main()
