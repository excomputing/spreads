import os

import numpy as np


class Nodes:

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def exc(s3_keys: list, bucket_name: str):
        """

        :param s3_keys:
        :param bucket_name:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        nodes = [f's3://{bucket_name}/{path}/*.csv' for path in paths]

        return nodes
