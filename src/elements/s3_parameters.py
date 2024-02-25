"""
This is data type S3Parameters
"""
import typing


class S3Parameters(typing.NamedTuple):
    """
    The data type class ⇾ S3Parameters

    Attributes
    ----------

    region_name
      * The Amazon Web Services region code.

    location_constraint
      * The region code of the region that the data is limited to.

    access_control_list
      * Access control list selection.

    bucket_name_int
      * The Amazon S3 (Simple Storage Service) bucket that hosts this project's data.

    path_int_points
      * The bucket path of the telemetric data.

    path_int_references
      * The bucket path of the telemetric data references.

    bucket_name_ext
      * The name of the bucket that the project's calculations will be delivered to

    path_ext_quantiles
      * The calculations path
    """

    region_name: str
    location_constraint: str
    access_control_list: str
    bucket_name_int: str
    path_int_points: str
    path_int_references: str
    bucket_name_ext: str
    path_ext_quantiles: str
