"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Configurations(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIN_NAMES_FIELD_NUMBER: builtins.int
    MULTI_SESSION_FIELD_NUMBER: builtins.int
    multi_session: builtins.bool
    @property
    def pin_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        pin_names: collections.abc.Iterable[builtins.str] | None = ...,
        multi_session: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["multi_session", b"multi_session", "pin_names", b"pin_names"]) -> None: ...

global___Configurations = Configurations

@typing.final
class Outputs(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIN_MAP_ID_FIELD_NUMBER: builtins.int
    SITES_FIELD_NUMBER: builtins.int
    SESSION_NAMES_FIELD_NUMBER: builtins.int
    RESOURCE_NAMES_FIELD_NUMBER: builtins.int
    CHANNEL_LISTS_FIELD_NUMBER: builtins.int
    pin_map_id: builtins.str
    @property
    def sites(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def session_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def resource_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def channel_lists(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        pin_map_id: builtins.str = ...,
        sites: collections.abc.Iterable[builtins.int] | None = ...,
        session_names: collections.abc.Iterable[builtins.str] | None = ...,
        resource_names: collections.abc.Iterable[builtins.str] | None = ...,
        channel_lists: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["channel_lists", b"channel_lists", "pin_map_id", b"pin_map_id", "resource_names", b"resource_names", "session_names", b"session_names", "sites", b"sites"]) -> None: ...

global___Outputs = Outputs
