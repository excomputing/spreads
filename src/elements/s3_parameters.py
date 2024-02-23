"""
This is data type S3Parameters
"""
import typing


class S3Parameters(typing.NamedTuple):
    """
    The data type class -> S3Parameters

    Attributes
    ----------

    region_name
      * The Amazon Web Services region code.

    location_constraint
      * The region code of the region that the data is limited to.

    access_control_list
      * Access control list selection.

    source_bucket_name
      * The Amazon S3 (Simple Storage Service) bucket that hosts this project's data.

    source_path_
      * The bucket path of the telemetric data.

    source_references_
      * The bucket path of the telemetric data references.

    source_n_references
      * The exact number of reference documents.

    delivery_bucket_name
      * The name of the bucket that the project's calculations will be delivered to

    delivery_path_
      * The calculations path
    """

    region_name: str
    location_constraint: str
    access_control_list: str
    source_bucket_name: str
    source_path_: str
    source_references_: str
    source_n_references: int
    delivery_bucket_name: str
    delivery_path_: str
