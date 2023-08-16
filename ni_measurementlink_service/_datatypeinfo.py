from typing import NamedTuple

from google.protobuf import type_pb2

from ni_measurementlink_service.measurement.info import DataType, TypeSpecialization


class DataTypeInfo(NamedTuple):
    """Class that represents the information for each of the DataType enum values.

    Attributes
    ----------
        grpc_field_type: Field.Kind associated with the DataType

        repeated: Whether the DataType is a repeated field

        type_specialization: Specific type when value_type
        can have more than one use

    """

    grpc_field_type: type_pb2.Field.Kind.ValueType
    repeated: bool
    type_specialization: TypeSpecialization = TypeSpecialization.NoType


def get_type_info(data_type: DataType) -> DataTypeInfo:
    """Get information about a DataType."""
    data_type_info = _DATATYPE_TO_DATATYPEINFO_LOOKUP.get(data_type)
    if data_type_info is None:
        raise Exception(f"Data type information not found '{data_type}'")
    return data_type_info


_DATATYPE_TO_DATATYPEINFO_LOOKUP = {
    DataType.Int32: DataTypeInfo(type_pb2.Field.TYPE_INT32, False),
    DataType.Int64: DataTypeInfo(type_pb2.Field.TYPE_INT64, False),
    DataType.UInt32: DataTypeInfo(type_pb2.Field.TYPE_UINT32, False),
    DataType.UInt64: DataTypeInfo(type_pb2.Field.TYPE_UINT64, False),
    DataType.Float: DataTypeInfo(type_pb2.Field.TYPE_FLOAT, False),
    DataType.Double: DataTypeInfo(type_pb2.Field.TYPE_DOUBLE, False),
    DataType.Boolean: DataTypeInfo(type_pb2.Field.TYPE_BOOL, False),
    DataType.String: DataTypeInfo(type_pb2.Field.TYPE_STRING, False),
    DataType.Pin: DataTypeInfo(type_pb2.Field.TYPE_STRING, False, TypeSpecialization.Pin),
    DataType.Path: DataTypeInfo(type_pb2.Field.TYPE_STRING, False, TypeSpecialization.Path),
    DataType.Enum: DataTypeInfo(type_pb2.Field.TYPE_ENUM, False, TypeSpecialization.Enum),
    DataType.Int32Array1D: DataTypeInfo(type_pb2.Field.TYPE_INT32, True),
    DataType.Int64Array1D: DataTypeInfo(type_pb2.Field.TYPE_INT64, True),
    DataType.UInt32Array1D: DataTypeInfo(type_pb2.Field.TYPE_UINT32, True),
    DataType.UInt64Array1D: DataTypeInfo(type_pb2.Field.TYPE_UINT64, True),
    DataType.FloatArray1D: DataTypeInfo(type_pb2.Field.TYPE_FLOAT, True),
    DataType.DoubleArray1D: DataTypeInfo(type_pb2.Field.TYPE_DOUBLE, True),
    DataType.BooleanArray1D: DataTypeInfo(type_pb2.Field.TYPE_BOOL, True),
    DataType.StringArray1D: DataTypeInfo(type_pb2.Field.TYPE_STRING, True),
    DataType.PinArray1D: DataTypeInfo(type_pb2.Field.TYPE_STRING, True, TypeSpecialization.Pin),
    DataType.PathArray1D: DataTypeInfo(type_pb2.Field.TYPE_STRING, True, TypeSpecialization.Path),
    DataType.EnumArray1D: DataTypeInfo(type_pb2.Field.TYPE_ENUM, True, TypeSpecialization.Enum),
}
