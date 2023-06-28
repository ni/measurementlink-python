"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
---------------------------------------------------------------------
---------------------------------------------------------------------
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ServiceDescriptor(google.protobuf.message.Message):
    """Description of a registered service. This information can be used to display information to the user
    about the service when services are being developed for a plugin architecture
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class AnnotationsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_URL_FIELD_NUMBER: builtins.int
    PROVIDED_INTERFACES_FIELD_NUMBER: builtins.int
    SERVICE_CLASS_FIELD_NUMBER: builtins.int
    ANNOTATIONS_FIELD_NUMBER: builtins.int
    display_name: builtins.str
    """Required. The user visible name of the service."""
    description_url: builtins.str
    """Optional. Url which provides descriptive information about the service"""
    @property
    def provided_interfaces(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Required. The service interfaces provided by the service. This is the gRPC Full Name of the service.
        Registration can use the gRPC metadata to provide these names.
        """
    service_class: builtins.str
    """Required. The "class" of a service. The value of this field should be unique for a given interface in provided_interfaces.
    In effect, the .proto service declaration defines the interface, and this field defines a class or concrete type of the interface.
    """
    @property
    def annotations(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Optional. Represents a set of annotations on the service.
        Well-known annotations:
        - Description
          - Key: "ni/service.description"
          - Expected format: string
          - Example: "Measure inrush current with a shorted load and validate results against configured limits."
        - Collection
          - Key: "ni/service.collection"
          - Expected format: "." delimited namespace/hierarchy case-insensitive string
          - Example: "CurrentTests.Inrush"
        - Tags
          - Key: "ni/service.tags"
          - Expected format: serialized JSON string of an array of strings
          - Example: "[\\"powerup\\", \\"current\\"]"
        """
    def __init__(
        self,
        *,
        display_name: builtins.str = ...,
        description_url: builtins.str = ...,
        provided_interfaces: collections.abc.Iterable[builtins.str] | None = ...,
        service_class: builtins.str = ...,
        annotations: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["annotations", b"annotations", "description_url", b"description_url", "display_name", b"display_name", "provided_interfaces", b"provided_interfaces", "service_class", b"service_class"]) -> None: ...

global___ServiceDescriptor = ServiceDescriptor

@typing_extensions.final
class ServiceLocation(google.protobuf.message.Message):
    """Represents the location of a service. The location generally includes the IP address and port number for the service
    which can be used to establish communication with the service.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOCATION_FIELD_NUMBER: builtins.int
    INSECURE_PORT_FIELD_NUMBER: builtins.int
    SSL_AUTHENTICATED_PORT_FIELD_NUMBER: builtins.int
    location: builtins.str
    """Required: The location of the service. This is typically an IP address or DNS name."""
    insecure_port: builtins.str
    """The port to use when communicating with the service for insecure HTTP connections. At least one of insecure_port or
    ssl_authenticated_port is required.
    """
    ssl_authenticated_port: builtins.str
    """The port to use when communicating with the service for secure SSL authenticated connections. At least one of
    insecure_port or ssl_authenticated_port is required.
    """
    def __init__(
        self,
        *,
        location: builtins.str = ...,
        insecure_port: builtins.str = ...,
        ssl_authenticated_port: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["insecure_port", b"insecure_port", "location", b"location", "ssl_authenticated_port", b"ssl_authenticated_port"]) -> None: ...

global___ServiceLocation = ServiceLocation

@typing_extensions.final
class RegisterServiceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SERVICE_DESCRIPTION_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def service_description(self) -> global___ServiceDescriptor:
        """Required. The description of the service."""
    @property
    def location(self) -> global___ServiceLocation:
        """Required. The canonical location information for the service."""
    def __init__(
        self,
        *,
        service_description: global___ServiceDescriptor | None = ...,
        location: global___ServiceLocation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["location", b"location", "service_description", b"service_description"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["location", b"location", "service_description", b"service_description"]) -> None: ...

global___RegisterServiceRequest = RegisterServiceRequest

@typing_extensions.final
class RegisterServiceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REGISTRATION_ID_FIELD_NUMBER: builtins.int
    registration_id: builtins.str
    """ID that can be used to unregister the service."""
    def __init__(
        self,
        *,
        registration_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["registration_id", b"registration_id"]) -> None: ...

global___RegisterServiceResponse = RegisterServiceResponse

@typing_extensions.final
class UnregisterServiceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REGISTRATION_ID_FIELD_NUMBER: builtins.int
    registration_id: builtins.str
    """Required. The registration ID of the service that should be unregistered."""
    def __init__(
        self,
        *,
        registration_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["registration_id", b"registration_id"]) -> None: ...

global___UnregisterServiceRequest = UnregisterServiceRequest

@typing_extensions.final
class UnregisterServiceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UnregisterServiceResponse = UnregisterServiceResponse

@typing_extensions.final
class EnumerateServicesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROVIDED_INTERFACE_FIELD_NUMBER: builtins.int
    provided_interface: builtins.str
    """Optional. The gRPC full name of the service interface that is needed. If empty,
    information for all services registered with the discovery service will be returned.
    """
    def __init__(
        self,
        *,
        provided_interface: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["provided_interface", b"provided_interface"]) -> None: ...

global___EnumerateServicesRequest = EnumerateServicesRequest

@typing_extensions.final
class EnumerateServicesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AVAILABLE_SERVICES_FIELD_NUMBER: builtins.int
    @property
    def available_services(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ServiceDescriptor]:
        """The list of available services which implement the specified service interface."""
    def __init__(
        self,
        *,
        available_services: collections.abc.Iterable[global___ServiceDescriptor] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["available_services", b"available_services"]) -> None: ...

global___EnumerateServicesResponse = EnumerateServicesResponse

@typing_extensions.final
class ResolveServiceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROVIDED_INTERFACE_FIELD_NUMBER: builtins.int
    SERVICE_CLASS_FIELD_NUMBER: builtins.int
    provided_interface: builtins.str
    """Required. This corresponds to the gRPC Full Name of the service and should match the information
    that was supplied in the RegisterServiceRequest message.
    """
    service_class: builtins.str
    """Optional. The service "class" that should be matched. If the value of this field is not specified and there
    is more than one matching service registered, an error is returned.
    """
    def __init__(
        self,
        *,
        provided_interface: builtins.str = ...,
        service_class: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["provided_interface", b"provided_interface", "service_class", b"service_class"]) -> None: ...

global___ResolveServiceRequest = ResolveServiceRequest
