import logging
import os
import sys


def main():

    # Logging
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    # Investigating bucket prefixes
    keys = src.s3.keys.Keys(service=service, s3_parameters=s3_parameters)
    items = keys.particular(
        prefix=s3_parameters.points_)
    logger.info(items)
    items = keys.all()
    logger.info(items)

    # The readings
    src.data.readings.Readings(s3_parameters=s3_parameters).exc()

    # Delete cache directories
    src.functions.cache.Cache().delete()


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.data.readings
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
