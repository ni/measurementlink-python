"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import ni_measurementlink_service._internal.stubs.ni.measurementlink.pinmap.v1.pin_map_service_pb2 as ni_measurementlink_pinmap_v1_pin_map_service_pb2

class PinMapServiceStub:
    """Service to keep track of pin map resources."""

    def __init__(self, channel: grpc.Channel) -> None: ...
    CreatePinMapFromXml: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.CreatePinMapFromXmlRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap,
    ]
    """Registers pin map with the PinMapService and returns a pin map resource.
    Status Codes for errors:
    - INVALID_ARGUMENT: Pin map id is empty or has whitespace, or pin map xml string is not valid
    - ALREADY_EXISTS: Pin map resource with the specified pin map id already exists
    """
    UpdatePinMapFromXml: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.UpdatePinMapFromXmlRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap,
    ]
    """Updates registered pin map contents and returns it.
    Creates and registers a pin map if a pin map resource for the specified pin map id is not found.
    Status Codes for errors:
    - INVALID_ARGUMENT: Pin map xml string is not valid
    """
    GetPinMap: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.GetPinMapRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap,
    ]
    """Get registered pin map resource.
    Status Codes for errors:
    - NOT_FOUND: Pin map resource for the specified pin map id is not found
    """
    QueryPins: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryPinsRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryPinsResponse,
    ]
    """Returns list of pins from the registered pin map resource.
    Status Codes for errors:
    - NOT_FOUND: Pin map resource for the specified pin map id is not found
    """
    QueryRelays: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryRelaysRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryRelaysResponse,
    ]
    """Returns list of relays from the registered pin map resource.
    Status Codes for errors:
    - NOT_FOUND: Pin map resource for the specified pin map id is not found
    """
    QueryResourceAccessInformation: grpc.UnaryUnaryMultiCallable[
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryResourceAccessInformationRequest,
        ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryResourceAccessInformationResponse,
    ]
    """Get instrument resource names, channels, and instrument type for the specified sites, pins or pin groups, relays or relay groups, instrument type in the registered pin map resource.
    Status Codes for errors:
    - NOT_FOUND:
      - Pin map resource for the specified pin map id is not found.
      - Specified site number is not in the valid range for the registered pin map.
    - INVALID_ARGUMENT:
      - Specified pin or relay is not present in the registered pin map resource.
      - Empty string specified for a pin or relay name.
    """

class PinMapServiceServicer(metaclass=abc.ABCMeta):
    """Service to keep track of pin map resources."""

    @abc.abstractmethod
    def CreatePinMapFromXml(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.CreatePinMapFromXmlRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap:
        """Registers pin map with the PinMapService and returns a pin map resource.
        Status Codes for errors:
        - INVALID_ARGUMENT: Pin map id is empty or has whitespace, or pin map xml string is not valid
        - ALREADY_EXISTS: Pin map resource with the specified pin map id already exists
        """
    @abc.abstractmethod
    def UpdatePinMapFromXml(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.UpdatePinMapFromXmlRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap:
        """Updates registered pin map contents and returns it.
        Creates and registers a pin map if a pin map resource for the specified pin map id is not found.
        Status Codes for errors:
        - INVALID_ARGUMENT: Pin map xml string is not valid
        """
    @abc.abstractmethod
    def GetPinMap(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.GetPinMapRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.PinMap:
        """Get registered pin map resource.
        Status Codes for errors:
        - NOT_FOUND: Pin map resource for the specified pin map id is not found
        """
    @abc.abstractmethod
    def QueryPins(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryPinsRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryPinsResponse:
        """Returns list of pins from the registered pin map resource.
        Status Codes for errors:
        - NOT_FOUND: Pin map resource for the specified pin map id is not found
        """
    @abc.abstractmethod
    def QueryRelays(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryRelaysRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryRelaysResponse:
        """Returns list of relays from the registered pin map resource.
        Status Codes for errors:
        - NOT_FOUND: Pin map resource for the specified pin map id is not found
        """
    @abc.abstractmethod
    def QueryResourceAccessInformation(
        self,
        request: ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryResourceAccessInformationRequest,
        context: grpc.ServicerContext,
    ) -> ni_measurementlink_pinmap_v1_pin_map_service_pb2.QueryResourceAccessInformationResponse:
        """Get instrument resource names, channels, and instrument type for the specified sites, pins or pin groups, relays or relay groups, instrument type in the registered pin map resource.
        Status Codes for errors:
        - NOT_FOUND:
          - Pin map resource for the specified pin map id is not found.
          - Specified site number is not in the valid range for the registered pin map.
        - INVALID_ARGUMENT:
          - Specified pin or relay is not present in the registered pin map resource.
          - Empty string specified for a pin or relay name.
        """

def add_PinMapServiceServicer_to_server(servicer: PinMapServiceServicer, server: grpc.Server) -> None: ...
