"""Parameter Serializer."""

import io
from ast import Bytes
from typing import Any, Dict, List

import ni_measurement_service._internal.parameter.serializationstrategy as serializationstrategy
from google.protobuf.internal import encoder
from ni_measurement_service._internal.parameter.metadata import ParameterMetadata


def deserialize_parameters(
    parameter_metadata_dict: Dict[id, ParameterMetadata], parameter_bytes: Bytes
) -> Dict[id, Any]:
    """Deserialize the bytes of the parameter based on the metadata.

    Args
    ----
        parameter_metadata_dict (Dict[id, ParameterMetadata]): Parameter metadata by ID.
        parameter_bytes (bytes): Bytes of Parameter that need to be deserialized.

    Returns
    -------
        Dict[id, Any]: Deserialized parameters by ID

    """
    # Getting overlapping parameters
    overlapping_parameter_by_id = _get_overlapping_parameters(
        parameter_metadata_dict, parameter_bytes
    )
    # Adding missing parameters with type defaults
    missing_parameters = _get_missing_parameters(
        parameter_metadata_dict, overlapping_parameter_by_id
    )
    overlapping_parameter_by_id.update(missing_parameters)
    return overlapping_parameter_by_id


def serialize_parameters(
    parameter_metadata_dict: Dict[id, ParameterMetadata], parameter_value: List[Any]
) -> Bytes:
    """Serialize the parameter values in same order based on the metadata_dict.

    Args
    ----
        parameter_metadata_dict (Dict[id, ParameterMetadata]): Parameter metadata by ID.
        parameter_value (_type_): List of Parameter values that need to be serialized.

    Returns
    -------
        Bytes: Serialized Bytes of Parameter Values.

    """
    serialize_buffer = io.BytesIO()  # inner_encoder updates the serialize_buffer
    for i, parameter in enumerate(parameter_value):
        parameter_metadata = parameter_metadata_dict[i + 1]
        encoder = serializationstrategy.Context.get_encoder(
            parameter_metadata.type,
            parameter_metadata.repeated,
        )
        type_default_value = serializationstrategy.Context.get_type_default(
            parameter_metadata.type,
            parameter_metadata.repeated,
        )
        # Skipping serialization if the value is None or if its a type default value.
        if parameter is not None and parameter != type_default_value:
            inner_encoder = encoder(i + 1)
            inner_encoder(serialize_buffer.write, parameter, None)
    return serialize_buffer.getvalue()


def serialize_default_values(parameter_metadata_dict: Dict[id, ParameterMetadata]) -> Bytes:
    """Serialize the Default values in the Metadata.

    Args
    -----
        parameter_metadata_dict (Dict[id, ParameterMetadata]): Configuration metadata.

    Returns
    -------
        Bytes: Serialized Bytes of default value.

    """
    default_value_parameter_array = list()
    for parameter in parameter_metadata_dict.values():
        parameter: ParameterMetadata
        default_value = parameter.default_value
        default_value_parameter_array.append(default_value)
    return serialize_parameters(parameter_metadata_dict, default_value_parameter_array)


def _get_field_index(parameter_bytes: Bytes, tag_position: int):
    """Get the Filed Index based on the tag's position.

    The tag Position should be the index of the TagValue in the ByteArray for valid field index.

    Args
    ----
        parameter_bytes (Bytes): _description_
        position (int): _description_

    Returns
    -------
        int: Filed index of the Tag Position

    """
    return parameter_bytes[tag_position] >> 3


def _get_overlapping_parameters(
    parameter_metadata_dict: Dict[id, ParameterMetadata], parameter_bytes: Bytes
) -> Dict[id, Any]:
    """Get the parameters present in both `parameter_metadata_dict` and `parameter_bytes`.

    Args
    ----
        parameter_metadata_dict (Dict[id, ParameterMetadata]): Parameter metadata by ID.
        parameter_bytes (bytes): Bytes of Parameter that need to be deserialized.

    Raises
    ------
        Exception: If the protobuf filed index is invalid.

    Returns
    -------
        Dict[id, Any]: Overlapping Parameters by ID.

    """
    overlapping_parameters_by_id = {}  # inner_decoder update the overlapping_parameters
    position = 0
    while position < len(parameter_bytes):
        field_index = _get_field_index(parameter_bytes, position)
        if field_index not in parameter_metadata_dict:
            raise Exception(
                f"Error occurred while reading the parameter - given protobuf index '{field_index}' is invalid."
            )
        type = parameter_metadata_dict[field_index].type
        is_repeated = parameter_metadata_dict[field_index].repeated
        decoder = serializationstrategy.Context.get_decoder(type, is_repeated)
        inner_decoder = decoder(field_index, field_index)
        parameter_bytes_io = io.BytesIO(parameter_bytes)
        parameter_bytes_memory_view = parameter_bytes_io.getbuffer()
        position = inner_decoder(
            parameter_bytes_memory_view,
            position + encoder._TagSize(field_index),
            len(parameter_bytes),
            type,
            overlapping_parameters_by_id,
        )
    return overlapping_parameters_by_id


def _get_missing_parameters(
    parameter_metadata_dict: Dict[id, ParameterMetadata], parameter_by_id: Dict[id, Any]
) -> Dict[id, Any]:
    """Get the Parameters defined in `parameter_metadata_dict` but not in `parameter_by_id`.

    Args
    ----
        parameter_metadata_dict (Dict[id, ParameterMetadata]): _description_
        parameter_by_id (Dict[id, Any]): Parameters by ID to compare the metadata with.

    Returns
    -------
        Dict[id, Any]: Missing parameter(as typedefaults) by ID.

    """
    missing_parameters = {}
    for key, value in parameter_metadata_dict.items():
        if key not in parameter_by_id:
            missing_parameters[value.name] = serializationstrategy.Context.get_type_default(
                value.type, value.repeated
            )
    return missing_parameters
