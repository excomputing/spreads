import os


class Config:

    def __init__(self):
        """
        Constructor

        s3://{bucket}/{prefix}/*.csv
        """

        self.storage = os.path.join(os.getcwd(), 'warehouse')
