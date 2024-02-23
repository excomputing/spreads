import logging
import os
import sys

import pandas as pd


def main():
    """
    The focus is the daily quantile spreads per station.  Note, the data sets of each
    telemetric device station are stored within a distinct Amazon S3 bucket node.

    Upcoming:
        * README.md Illustration
        * Does the delivery bucket exist?

    :return:
    """

    # Logging
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    # Branches
    branches = src.algorithms.branches.Branches(service=service, s3_parameters=s3_parameters).exc()

    # References
    references: pd.DataFrame = src.algorithms.references.References(service=service, s3_parameters=s3_parameters).exc()

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

    # Modules
    import config
    import src.algorithms.interface
    import src.algorithms.branches
    import src.algorithms.references
    import src.s3.bucket
    import src.s3.objects
    import src.elements.s3_parameters as s3p
    import src.elements.service as sr
    import src.functions.cache
    import src.functions.directories
    import src.functions.service
    import src.s3.s3_parameters

    # S3 S3Parameters, Service Instance
    s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters().exc()
    service: sr.Service = src.functions.service.Service(region_name=s3_parameters.region_name).exc()

    # Warehouse
    storage = config.Config().storage
    directories = src.functions.directories.Directories()
    directories.cleanup(path=storage)
    directories.create(path=storage)

    # Amazon
    bucket = src.s3.bucket.Bucket(service=service, location_constraint=s3_parameters.location_constraint,
                                  bucket_name=s3_parameters.delivery_bucket_name)
    objects = src.s3.objects.Objects(service=service, bucket_name=s3_parameters.delivery_bucket_name)
    iterable = objects.filter(prefix=s3_parameters.delivery_path_)

    if bucket.exists():
        iterable.delete()
    else:
        bucket.create()

    main()
