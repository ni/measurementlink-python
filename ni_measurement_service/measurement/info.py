"""Contains classes and enums to represent measurement metadata."""
from __future__ import annotations

import enum
import typing
from pathlib import Path
from typing import NamedTuple

from google.protobuf import type_pb2


class MeasurementInfo(NamedTuple):
    """Class that represents the measurement information.

    Attributes
    ----------
        display_name (str): The measurement display name for client to display to user.

        version (str): The measurement version that helps to
        maintain versions of a measurement in future.

        ui_file_paths (list): Absolute paths of the UI file(s) linked to the measurement.

    """

    display_name: str
    version: str
    ui_file_paths: typing.List[Path]


class ServiceInfo(NamedTuple):
    """Class the represents the service information.

    Attributes
    ----------
        service_class (str): Service class that the measurement belongs to.
        Measurements under same service class expected to perform same logic.
        For e.g., different version of measurement can come under same service class.

        description_url (str): Description URL of the measurement.

    """

    service_class: str
    description_url: str

class TypeSpecialization(enum.Enum):
    '''Represents the different type specializations for measurement parameters'''

    No_Type = ""
    Pin = "pin"

class DataType(enum.Enum):
    """Enum that represents the supported data types."""

    Int32 = (type_pb2.Field.TYPE_INT32, False, TypeSpecialization.No_Type)
    Int64 = (type_pb2.Field.TYPE_INT64, False, TypeSpecialization.No_Type)
    UInt32 = (type_pb2.Field.TYPE_UINT32, False, TypeSpecialization.No_Type)
    UInt64 = (type_pb2.Field.TYPE_UINT64, False, TypeSpecialization.No_Type)
    Float = (type_pb2.Field.TYPE_FLOAT, False, TypeSpecialization.No_Type)
    Double = (type_pb2.Field.TYPE_DOUBLE, False, TypeSpecialization.No_Type)
    Boolean = (type_pb2.Field.TYPE_BOOL, False, TypeSpecialization.No_Type)
    String = (type_pb2.Field.TYPE_STRING, False, TypeSpecialization.No_Type)
    Pin = (type_pb2.Field.TYPE_STRING, False, TypeSpecialization.Pin)

    Int32Array1D = (type_pb2.Field.TYPE_INT32, True, TypeSpecialization.No_Type)
    Int64Array1D = (type_pb2.Field.TYPE_INT64, True, TypeSpecialization.No_Type)
    UInt32Array1D = (type_pb2.Field.TYPE_UINT32, True, TypeSpecialization.No_Type)
    UInt64Array1D = (type_pb2.Field.TYPE_UINT64, True, TypeSpecialization.No_Type)
    FloatArray1D = (type_pb2.Field.TYPE_FLOAT, True, TypeSpecialization.No_Type)
    DoubleArray1D = (type_pb2.Field.TYPE_DOUBLE, True, TypeSpecialization.No_Type)
    BooleanArray1D = (type_pb2.Field.TYPE_BOOL, True, TypeSpecialization.No_Type)


