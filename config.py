"""Module config.py"""
import os


class Config:
    """
    Configurations
    """

    def __init__(self):
        """
        Constructor

        s3://{bucket}/{prefix}/*.csv
        """

        # Local results storage area
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.storage = os.path.join(self.warehouse, 'spreads')

        # A S3 parameters template
        self.s3_parameters_key = 's3_parameters.yaml'

        # The metadata of the resulting JSON files.
        self.metadata = {
            'attributes': 'Brief [telemetric device] raw data source details.',
            'columns': 'The columns of each data instance.',
            'data': 'The data instances.  Each instance records the quantiles and extrema calculations of a day.'}
