import logging
import os
import sys

import pandas as pd


def main():
    """
    The focus is the daily quantile spreads per station.  Note, the data sets of each
    telemetric device station are stored within a distinct Amazon S3 bucket node.

    Upcoming: README.md Illustration

    :return:
    """

    # Logging
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    # The list of keys, i.e., CSV files, that store telemetric data
    s3_keys = src.s3.keys.Keys(
        service=service, s3_parameters=s3_parameters).particular(prefix=s3_parameters.points_)

    # The nodes, i.e., the distinct paths
    nodes: list = src.algorithms.nodes.Nodes(
        s3_parameters=s3_parameters).exc(s3_keys=s3_keys)

    references: pd.DataFrame = src.algorithms.references.References(
        service=service, s3_parameters=s3_parameters).exc()

    # The readings
    src.algorithms.interface.Interface().exc(nodes=nodes, references=references)

    # Delete cache directories
    src.functions.cache.Cache().delete()


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.algorithms.interface
    import src.algorithms.nodes
    import src.algorithms.references
    import src.elements.s3_parameters as s3p
    import src.elements.service as sr
    import src.functions.cache
    import src.functions.service
    import src.s3.keys
    import src.s3.s3_parameters

    # S3 S3Parameters, Service Instance
    s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters().exc()
    service: sr.Service = src.functions.service.Service(region_name=s3_parameters.region_name).exc()


    main()
