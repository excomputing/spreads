import logging
import os
import sys


def main():

    # Logging
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    # Objective: Daily quantile spreads per station
    # Note: The data sets of each telemetric device station are stored within its distinct S3 bucket node.
    # Hence: Retrieve the data sets by node [Upcoming: README.md Diagram]
    # bucket prefixes
    keys = src.s3.keys.Keys(service=service, s3_parameters=s3_parameters)
    s3_keys: list = keys.particular(prefix=s3_parameters.points_)

    # The readings
    src.algorithms.interface.Interface(s3_parameters=s3_parameters).exc(s3_keys=s3_keys)

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
