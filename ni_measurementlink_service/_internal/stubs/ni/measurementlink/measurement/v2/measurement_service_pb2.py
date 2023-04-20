# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ni/measurementlink/measurement/v2/measurement_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import type_pb2 as google_dot_protobuf_dot_type__pb2
from ni_measurementlink_service._internal.stubs.ni.measurementlink import (
    pin_map_context_pb2 as ni_dot_measurementlink_dot_pin__map__context__pb2,
)


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n;ni/measurementlink/measurement/v2/measurement_service.proto\x12!ni.measurementlink.measurement.v2\x1a\x19google/protobuf/any.proto\x1a\x1agoogle/protobuf/type.proto\x1a(ni/measurementlink/pin_map_context.proto"\x14\n\x12GetMetadataRequest"\x9a\x02\n\x13GetMetadataResponse\x12R\n\x13measurement_details\x18\x01 \x01(\x0b\x32\x35.ni.measurementlink.measurement.v2.MeasurementDetails\x12V\n\x15measurement_signature\x18\x02 \x01(\x0b\x32\x37.ni.measurementlink.measurement.v2.MeasurementSignature\x12W\n\x16user_interface_details\x18\x03 \x03(\x0b\x32\x37.ni.measurementlink.measurement.v2.UserInterfaceDetails"\x84\x01\n\x0eMeasureRequest\x12\x36\n\x18\x63onfiguration_parameters\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\x12:\n\x0fpin_map_context\x18\x02 \x01(\x0b\x32!.ni.measurementlink.PinMapContext"8\n\x0fMeasureResponse\x12%\n\x07outputs\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any";\n\x12MeasurementDetails\x12\x14\n\x0c\x64isplay_name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t"\xb2\x02\n\x14MeasurementSignature\x12-\n%configuration_parameters_message_type\x18\x01 \x01(\t\x12[\n\x18\x63onfiguration_parameters\x18\x02 \x03(\x0b\x32\x39.ni.measurementlink.measurement.v2.ConfigurationParameter\x12\x34\n\x16\x63onfiguration_defaults\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x1c\n\x14outputs_message_type\x18\x04 \x01(\t\x12:\n\x07outputs\x18\x05 \x03(\x0b\x32).ni.measurementlink.measurement.v2.Output"(\n\x14UserInterfaceDetails\x12\x10\n\x08\x66ile_url\x18\x01 \x01(\t"\x8e\x02\n\x16\x43onfigurationParameter\x12\x14\n\x0c\x66ield_number\x18\x01 \x01(\x05\x12)\n\x04type\x18\x02 \x01(\x0e\x32\x1b.google.protobuf.Field.Kind\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08repeated\x18\x04 \x01(\x08\x12_\n\x0b\x61nnotations\x18\x05 \x03(\x0b\x32J.ni.measurementlink.measurement.v2.ConfigurationParameter.AnnotationsEntry\x1a\x32\n\x10\x41nnotationsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xee\x01\n\x06Output\x12\x14\n\x0c\x66ield_number\x18\x01 \x01(\x05\x12)\n\x04type\x18\x02 \x01(\x0e\x32\x1b.google.protobuf.Field.Kind\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08repeated\x18\x04 \x01(\x08\x12O\n\x0b\x61nnotations\x18\x05 \x03(\x0b\x32:.ni.measurementlink.measurement.v2.Output.AnnotationsEntry\x1a\x32\n\x10\x41nnotationsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\x86\x02\n\x12MeasurementService\x12|\n\x0bGetMetadata\x12\x35.ni.measurementlink.measurement.v2.GetMetadataRequest\x1a\x36.ni.measurementlink.measurement.v2.GetMetadataResponse\x12r\n\x07Measure\x12\x31.ni.measurementlink.measurement.v2.MeasureRequest\x1a\x32.ni.measurementlink.measurement.v2.MeasureResponse0\x01\x42\xd8\x01\n%com.ni.measurementlink.measurement.v2B\x17MeasurementServiceProtoP\x01Z\rmeasurementv2\xa2\x02\x04NIMM\xaa\x02\x32NationalInstruments.MeasurementLink.Measurement.V2\xca\x02!NI\\MeasurementLink\\Measurement\\V2\xea\x02$NI::MeasurementLink::Measurement::V2b\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "ni.measurementlink.measurement.v2.measurement_service_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n%com.ni.measurementlink.measurement.v2B\027MeasurementServiceProtoP\001Z\rmeasurementv2\242\002\004NIMM\252\0022NationalInstruments.MeasurementLink.Measurement.V2\312\002!NI\\MeasurementLink\\Measurement\\V2\352\002$NI::MeasurementLink::Measurement::V2"
    _CONFIGURATIONPARAMETER_ANNOTATIONSENTRY._options = None
    _CONFIGURATIONPARAMETER_ANNOTATIONSENTRY._serialized_options = b"8\001"
    _OUTPUT_ANNOTATIONSENTRY._options = None
    _OUTPUT_ANNOTATIONSENTRY._serialized_options = b"8\001"
    _GETMETADATAREQUEST._serialized_start = 195
    _GETMETADATAREQUEST._serialized_end = 215
    _GETMETADATARESPONSE._serialized_start = 218
    _GETMETADATARESPONSE._serialized_end = 500
    _MEASUREREQUEST._serialized_start = 503
    _MEASUREREQUEST._serialized_end = 635
    _MEASURERESPONSE._serialized_start = 637
    _MEASURERESPONSE._serialized_end = 693
    _MEASUREMENTDETAILS._serialized_start = 695
    _MEASUREMENTDETAILS._serialized_end = 754
    _MEASUREMENTSIGNATURE._serialized_start = 757
    _MEASUREMENTSIGNATURE._serialized_end = 1063
    _USERINTERFACEDETAILS._serialized_start = 1065
    _USERINTERFACEDETAILS._serialized_end = 1105
    _CONFIGURATIONPARAMETER._serialized_start = 1108
    _CONFIGURATIONPARAMETER._serialized_end = 1378
    _CONFIGURATIONPARAMETER_ANNOTATIONSENTRY._serialized_start = 1328
    _CONFIGURATIONPARAMETER_ANNOTATIONSENTRY._serialized_end = 1378
    _OUTPUT._serialized_start = 1381
    _OUTPUT._serialized_end = 1619
    _OUTPUT_ANNOTATIONSENTRY._serialized_start = 1328
    _OUTPUT_ANNOTATIONSENTRY._serialized_end = 1378
    _MEASUREMENTSERVICE._serialized_start = 1622
    _MEASUREMENTSERVICE._serialized_end = 1884
# @@protoc_insertion_point(module_scope)
