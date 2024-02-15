import logging
import os
import sys


def main():
    logger = logging.getLogger(__name__)
    logger.info('Spreads')

    src.data.readings.Readings(s3_parameters=s3_parameters).exc()


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
    import src.functions.service
    import src.s3.s3_parameters

    # S3 S3Parameters, Service Instance
    s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters().exc()
    service: sr.Service = src.functions.service.Service(region_name=s3_parameters.region_name).exc()

    main()
