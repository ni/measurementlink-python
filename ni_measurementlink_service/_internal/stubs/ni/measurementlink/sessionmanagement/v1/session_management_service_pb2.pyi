"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import ni_measurementlink_service._internal.stubs.ni.measurementlink.pin_map_context_pb2 as ni_measurementlink_pin_map_context_pb2
from ni_measurementlink_service._internal.stubs import session_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class SessionInformation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_FIELD_NUMBER: builtins.int
    RESOURCE_NAME_FIELD_NUMBER: builtins.int
    CHANNEL_LIST_FIELD_NUMBER: builtins.int
    INSTRUMENT_TYPE_ID_FIELD_NUMBER: builtins.int
    SESSION_EXISTS_FIELD_NUMBER: builtins.int
    CHANNEL_MAPPINGS_FIELD_NUMBER: builtins.int
    @property
    def session(self) -> session_pb2.Session:
        """Session identifier used to identify the session in the session management service, as well as in driver services such as grpc-device.
        This field is readonly.
        """
    resource_name: builtins.str
    """Resource name used to open this session in the driver.
    This field is readonly.
    """
    channel_list: builtins.str
    """Channel list used for driver initialization and measurement methods.
    This field is empty for any SessionInformation returned from ReserveAllRegisteredSessions.
    This field is readonly.
    """
    instrument_type_id: builtins.str
    """Instrument type ID to identify which type of instrument the session represents.
    Pin maps have built in instrument definitions using the following NI driver based instrument type ids:
         "niDCPower"
         "niDigitalPattern"
         "niScope"
         "niDMM"
         "niDAQmx"
         "niFGen"
         "niRelayDriver"
    For custom instruments the user defined instrument type id is defined in the pin map file.
    This field is readonly.
    """
    session_exists: builtins.bool
    """Indicates whether the session exists in the Session Manager. This indicates whether the session has been created.
    This field is readonly.
    """
    @property
    def channel_mappings(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChannelMapping
    ]:
        """List of site and pin/relay mappings that correspond to each channel in the channel_list.
        Each item contains a mapping corresponding to a channel in this instrument resource, in the order of the channel_list.
        This field is empty for any SessionInformation returned from ReserveAllRegisteredSessions.
        This field is readonly.
        """
    def __init__(
        self,
        *,
        session: session_pb2.Session | None = ...,
        resource_name: builtins.str = ...,
        channel_list: builtins.str = ...,
        instrument_type_id: builtins.str = ...,
        session_exists: builtins.bool = ...,
        channel_mappings: collections.abc.Iterable[global___ChannelMapping] | None = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["session", b"session"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "channel_list",
            b"channel_list",
            "channel_mappings",
            b"channel_mappings",
            "instrument_type_id",
            b"instrument_type_id",
            "resource_name",
            b"resource_name",
            "session",
            b"session",
            "session_exists",
            b"session_exists",
        ],
    ) -> None: ...

global___SessionInformation = SessionInformation

@typing_extensions.final
class ChannelMapping(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIN_OR_RELAY_NAME_FIELD_NUMBER: builtins.int
    SITE_FIELD_NUMBER: builtins.int
    CHANNEL_FIELD_NUMBER: builtins.int
    pin_or_relay_name: builtins.str
    """The pin or relay that is mapped to a channel."""
    site: builtins.int
    """The site on which the pin or relay is mapped to a channel.
    For system pins/relays the site number is -1 since they do not belong to a specific site.
    """
    channel: builtins.str
    """The channel to which the pin or relay is mapped on this site."""
    def __init__(
        self,
        *,
        pin_or_relay_name: builtins.str = ...,
        site: builtins.int = ...,
        channel: builtins.str = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "channel", b"channel", "pin_or_relay_name", b"pin_or_relay_name", "site", b"site"
        ],
    ) -> None: ...

global___ChannelMapping = ChannelMapping

@typing_extensions.final
class ReserveSessionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIN_MAP_CONTEXT_FIELD_NUMBER: builtins.int
    PIN_OR_RELAY_NAMES_FIELD_NUMBER: builtins.int
    INSTRUMENT_TYPE_ID_FIELD_NUMBER: builtins.int
    TIMEOUT_IN_MILLISECONDS_FIELD_NUMBER: builtins.int
    @property
    def pin_map_context(self) -> ni_measurementlink_pin_map_context_pb2.PinMapContext:
        """Required. Includes the pin map ID for the pin map in the Pin Map Service, as well as the list of sites for the measurement."""
    @property
    def pin_or_relay_names(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Optional. List of pins, pin groups, relays, or relay groups to use for the measurement. If unspecified, reserve sessions for all pins and relays in the registered pin map resource."""
    instrument_type_id: builtins.str
    """Optional. Instrument type ID for the measurement. If unspecified, reserve sessions for all instrument types connected in the registered pin map resource.
    Pin maps have built in instrument definitions using the following NI driver based instrument type ids:
         "niDCPower"
         "niDigitalPattern"
         "niScope"
         "niDMM"
         "niDAQmx"
         "niFGen"
         "niRelayDriver"
    For custom instruments the user defined instrument type id is defined in the pin map file.
    """
    timeout_in_milliseconds: builtins.int
    """Optional. Timeout for the reservation request.
    Allowed values: 0 (non-blocking, fails immediately if resources cannot be reserved), -1 (infinite timeout), or any other positive numeric value (wait for that number of milliseconds)
    """
    def __init__(
        self,
        *,
        pin_map_context: ni_measurementlink_pin_map_context_pb2.PinMapContext | None = ...,
        pin_or_relay_names: collections.abc.Iterable[builtins.str] | None = ...,
        instrument_type_id: builtins.str = ...,
        timeout_in_milliseconds: builtins.int = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["pin_map_context", b"pin_map_context"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "instrument_type_id",
            b"instrument_type_id",
            "pin_map_context",
            b"pin_map_context",
            "pin_or_relay_names",
            b"pin_or_relay_names",
            "timeout_in_milliseconds",
            b"timeout_in_milliseconds",
        ],
    ) -> None: ...

global___ReserveSessionsRequest = ReserveSessionsRequest

@typing_extensions.final
class ReserveSessionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSIONS_FIELD_NUMBER: builtins.int
    @property
    def sessions(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___SessionInformation
    ]:
        """List of information needed to create or use each session for the given pin, site, and instrument type ID.
        This field is readonly.
        """
    def __init__(
        self,
        *,
        sessions: collections.abc.Iterable[global___SessionInformation] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["sessions", b"sessions"]
    ) -> None: ...

global___ReserveSessionsResponse = ReserveSessionsResponse

@typing_extensions.final
class UnreserveSessionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSIONS_FIELD_NUMBER: builtins.int
    @property
    def sessions(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___SessionInformation
    ]:
        """Required. List of information of sessions to be unreserved in the session management service."""
    def __init__(
        self,
        *,
        sessions: collections.abc.Iterable[global___SessionInformation] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["sessions", b"sessions"]
    ) -> None: ...

global___UnreserveSessionsRequest = UnreserveSessionsRequest

@typing_extensions.final
class UnreserveSessionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UnreserveSessionsResponse = UnreserveSessionsResponse

@typing_extensions.final
class RegisterSessionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSIONS_FIELD_NUMBER: builtins.int
    @property
    def sessions(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___SessionInformation
    ]:
        """Required. List of sessions to register with the session management service to track as the sessions are open."""
    def __init__(
        self,
        *,
        sessions: collections.abc.Iterable[global___SessionInformation] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["sessions", b"sessions"]
    ) -> None: ...

global___RegisterSessionsRequest = RegisterSessionsRequest

@typing_extensions.final
class RegisterSessionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___RegisterSessionsResponse = RegisterSessionsResponse

@typing_extensions.final
class UnregisterSessionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSIONS_FIELD_NUMBER: builtins.int
    @property
    def sessions(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___SessionInformation
    ]:
        """Required. List of sessions to unregister with the session management service to mark them as sessions were closed."""
    def __init__(
        self,
        *,
        sessions: collections.abc.Iterable[global___SessionInformation] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["sessions", b"sessions"]
    ) -> None: ...

global___UnregisterSessionsRequest = UnregisterSessionsRequest

@typing_extensions.final
class UnregisterSessionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UnregisterSessionsResponse = UnregisterSessionsResponse

@typing_extensions.final
class ReserveAllRegisteredSessionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMEOUT_IN_MILLISECONDS_FIELD_NUMBER: builtins.int
    INSTRUMENT_TYPE_ID_FIELD_NUMBER: builtins.int
    timeout_in_milliseconds: builtins.int
    """Optional. Timeout for the reservation request.
    Allowed values: 0 (non-blocking, fails immediately if resources cannot be reserved), -1 (infinite timeout), or any other positive numeric value (wait for that number of milliseconds)
    """
    instrument_type_id: builtins.str
    """Optional. Instrument type ID of the registered sessions to reserve. If unspecified, reserve sessions for all instrument types connected in the registered pin map resource.
    Pin maps have built in instrument definitions using the following NI driver based instrument type ids:
         "niDCPower"
         "niDigitalPattern"
         "niScope"
         "niDMM"
         "niDAQmx"
         "niFGen"
         "niRelayDriver"
    For custom instruments the user defined instrument type id is defined in the pin map file.
    """
    def __init__(
        self,
        *,
        timeout_in_milliseconds: builtins.int = ...,
        instrument_type_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "instrument_type_id",
            b"instrument_type_id",
            "timeout_in_milliseconds",
            b"timeout_in_milliseconds",
        ],
    ) -> None: ...

global___ReserveAllRegisteredSessionsRequest = ReserveAllRegisteredSessionsRequest

@typing_extensions.final
class ReserveAllRegisteredSessionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSIONS_FIELD_NUMBER: builtins.int
    @property
    def sessions(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___SessionInformation
    ]:
        """Sessions currently registered in the session management service."""
    def __init__(
        self,
        *,
        sessions: collections.abc.Iterable[global___SessionInformation] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["sessions", b"sessions"]
    ) -> None: ...

global___ReserveAllRegisteredSessionsResponse = ReserveAllRegisteredSessionsResponse
