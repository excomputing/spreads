"""
This is data type S3Parameters
"""
import typing


class S3Parameters(typing.NamedTuple):
    """
    The data type class -> S3Parameters

    Attributes
    ----------
    region_name : str
      The Amazon Web Services region code.

    location_constraint : str
      The region code of the region that the data is limited to.

    access_control_list : str
      Access control list selection.

    bucket_name : str
      The Amazon S3 (Simple Storage Service) bucket that hosts this project's data.

    points_ : str
      The bucket path of the telemetric data.

    references_ : str
      The bucket path of the telemetric data references.

    n_references : int
      The exact number of reference documents.
    """

    region_name: str
    location_constraint: str
    access_control_list: str
    bucket_name: str
    points_: str
    references_: str
    n_references: int
