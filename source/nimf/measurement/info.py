"""Contains classes and enums to represent measurement metadata."""

import enum
from typing import NamedTuple

import google.protobuf.type_pb2 as type_pb2


class UIFileType(enum.Enum):
    """Enum that represents the supported UI Types."""

    ScreenFile = "ni_scr://"
    LabVIEW = "ni_vi://"


class MeasurementInfo(NamedTuple):
    """Class that represents the measurement information.

    Attributes
    ----------
        display_name (str): The display name of the measurement.
        version (str): The version of the measurement.
        measurement_type (str): Type of the measurement.
        product_type (str): Type of product related to the measurement.
        ui_file_path (str): Path of the UI file linked to the measurement.
        ui_file_type (UIFileType): Type of the linked UI file.

    """

    display_name: str = None
    version: str = None
    measurement_type: str = None
    product_type: str = None
    ui_file_path: str = None
    ui_file_type: UIFileType = None


class ServiceInfo(NamedTuple):
    """Class the represts the service information.

    Attributes
    ----------
        service_class (str): Service class that the measurement belongs to.
        Measurements under same service class expected to perform same logic.
        For e.g., different version of measurement can come under same service class.
        service_id (str): Unique service of the measurement. Should be an Unique GUID.
        description_url (str): Description URL of the measurement.

    """

    service_class: str
    service_id: str
    description_url: str


class DataType(enum.Enum):
    """Enum that represents the suppported data types."""

    Int32 = (type_pb2.Field.TYPE_INT32, False)
    Int64 = (type_pb2.Field.TYPE_INT64, False)
    UInt32 = (type_pb2.Field.TYPE_UINT32, False)
    UInt64 = (type_pb2.Field.TYPE_UINT64, False)
    Float = (type_pb2.Field.TYPE_FLOAT, False)
    Double = (type_pb2.Field.TYPE_DOUBLE, False)
    Boolean = (type_pb2.Field.TYPE_BOOL, False)
    String = (type_pb2.Field.TYPE_STRING, False)

    DoubleArray1D = (type_pb2.Field.TYPE_DOUBLE, True)
