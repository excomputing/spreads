import os


class Config:

    def __init__(self):
        """
        Constructor

        s3://{bucket}/{prefix}/*.csv
        """

        self.storage = os.path.join(os.getcwd(), 'warehouse')

        self.metadata = {
            'attributes': 'Brief [telemetric device] raw data source details.',
            'columns': 'The columns of each data instance.',
            'data': 'The data instances.  Each instance records the quantiles and extrema calculations of a day.'}
