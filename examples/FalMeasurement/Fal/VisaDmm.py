from __future__ import annotations

import contextlib
import pathlib

import ni_measurementlink_service as nims
from decouple import AutoConfig
import logging

from decouple import AutoConfig
from ni_measurementlink_service.discovery import DiscoveryClient
from ni_measurementlink_service.session_management import (
    SessionInformation,
    SessionInitializationBehavior,
    SingleSessionReservation,
)

import sys
from enum import Enum
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type

import pyvisa
import pyvisa.resources
import pyvisa.typing
from urllib.parse import urlencode, urlsplit


_INITIALIZATION_BEHAVIOR = {
    SessionInitializationBehavior.AUTO: 0,
    SessionInitializationBehavior.INITIALIZE_SERVER_SESSION: 1,
    SessionInitializationBehavior.ATTACH_TO_SERVER_SESSION: 2,
    SessionInitializationBehavior.INITIALIZE_SESSION_THEN_DETACH: 3,
    SessionInitializationBehavior.ATTACH_TO_SESSION_THEN_CLOSE: 4,
}

GRPC_SERVICE_INTERFACE_NAME = "visa_grpc.Visa"
SERVICE_CLASS = "ni.measurementlink.v1.grpcdeviceserver"


if TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


# Pin map instrument type constant for VISA DMM
INSTRUMENT_TYPE_VISA_DMM = "VisaDmm"

_SIMULATION_YAML_PATH = pathlib.Path(__file__).resolve().parent / "_visa_dmm_sim.yaml"

_RESOLUTION_DIGITS_TO_VALUE = {"3.5": 0.001, "4.5": 0.0001, "5.5": 1e-5, "6.5": 1e-6}

# Supported NI-VISA DMM instrument IDs, both real and simulated, can be added here
_SUPPORTED_INSTRUMENT_IDS = [
    # Keysight/Agilent/HP 34401A
    "34401",
    "34410",
    "34411",
    "L4411",
    # NI Instrument Simulator v2.0
    "Instrument Simulator",  # single instrument
    "Waveform Generator Simulator",  # multi-instrument
]


class Function(Enum):
    """Enum that represents the measurement function."""

    DC_VOLTS = 1
    AC_VOLTS = 2


_FUNCTION_TO_VALUE = {
    Function.DC_VOLTS: "VOLT:DC",
    Function.AC_VOLTS: "VOLT:AC",
}


# Search for the `.env` file starting with the current directory.
_config = AutoConfig(str(pathlib.Path.cwd()))
_logger = logging.getLogger(__name__)


class VisaDmm():
    """An NI-VISA DMM Implementation."""
    @contextlib.contextmanager
    def initialize(self, reservation : SingleSessionReservation, measurement_service: nims.MeasurementService):
        """Initialize a single NI-VISA DMM instrument session."""
        session_constructor = VisaDmmSessionConstructor(_config, measurement_service.discovery_client)

        with reservation.initialize_session(
            session_constructor, INSTRUMENT_TYPE_VISA_DMM
        ) as session_info:            
            self._session = session_info.session
            yield self._session


    def configure(self, measurement_function, range, resolution_digits):
        visa_dmm_function = Function(measurement_function.value)
        self._session.configure_measurement_digits(visa_dmm_function, range, resolution_digits)

   
    def measure(self):
        return self._session.read()


class VisaDmmSessionConstructor:
    """MeasurementLink session constructor for VISA DMM sessions."""

    def __init__(
        self,
        config: AutoConfig,
        discovery_client: DiscoveryClient,
        initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.AUTO,
    ) -> None:
        """Construct a VisaDmmSessionConstructor."""
        self._config = config
        self._discovery_client = discovery_client
        self._initialization_behavior = initialization_behavior

        # Hack: config is a parameter for now so TestStand code modules use the right config path.
        self._visa_dmm_simulate: bool = config(
            "MEASUREMENTLINK_VISA_DMM_SIMULATE", default=False, cast=bool
        )

        if self._visa_dmm_simulate:
            # _visa_dmm_sim.yaml doesn't include the grpc:// resource names.
            _logger.debug("Not using NI gRPC Device Server due to simulation")
            self._address = ""
        else:
            self._address = get_visa_grpc_insecure_address(config, discovery_client)
            if self._address:
                _logger.debug("NI gRPC Device Server address: http://%s", self._address)
            else:
                _logger.debug("Not using NI gRPC Device Server")

    def __call__(self, session_info: SessionInformation) -> Session:
        """Construct a VISA DMM session based on MeasurementLink session info."""
        resource_name = session_info.resource_name
        if self._address:
            resource_name = build_visa_grpc_resource_string(
                resource_name,
                self._address,
                session_info.session_name,
                self._initialization_behavior,
            )

        # When this measurement is called from outside of TestStand (session_exists
        # == False), reset the instrument to a known state. In TestStand,
        # ProcessSetup resets the instrument.
        reset_device = not session_info.session_exists

        _logger.debug("VISA resource name: %s", resource_name)
        return Session(resource_name, reset_device=reset_device, simulate=self._visa_dmm_simulate)


class Session:
    """An NI-VISA DMM session."""

    def __init__(
        self,
        resource_name: str,
        id_query: bool = True,
        reset_device: bool = True,
        simulate: bool = False,
    ) -> None:
        """Open NI-VISA DMM session."""
        # Create a real or simulated VISA resource manager."""
        visa_library = f"{_SIMULATION_YAML_PATH}@sim" if simulate else ""
        resource_manager = pyvisa.ResourceManager(visa_library)

        session = resource_manager.open_resource(
            resource_name, read_termination="\n", write_termination="\n"
        )

        if not isinstance(session, pyvisa.resources.MessageBasedResource):
            raise TypeError("The 'session' object must be an instance of MessageBasedResource.")
        self._session = session

        if id_query:
            self._validate_id()

        if reset_device:
            self._reset()

    def close(self) -> None:
        """Close the session."""
        self._session.close()

    def __enter__(self) -> Self:
        """Context management protocol. Returns self."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Context management protocol. Calls close()."""
        self.close()

    def configure_measurement_digits(
        self, function: Function, range: float, resolution_digits: float
    ) -> None:
        """Configure the common properties of the measurement.

        These properties include function, range, and resolution_digits.
        """
        function_enum = _FUNCTION_TO_VALUE[function]
        resolution_value = _RESOLUTION_DIGITS_TO_VALUE[str(resolution_digits)]

        self._session.write("CONF:%s %.g,%.g" % (function_enum, range, resolution_value))
        self._check_error()

    def read(self) -> float:
        """Acquires a single measurement and returns the measured value."""
        response = self._session.query("READ?")
        self._check_error()
        return float(response)

    def _check_error(self) -> None:
        """Query the instrument's error queue."""
        response = self._session.query("SYST:ERR?")
        fields = response.split(",", maxsplit=1)
        assert len(fields) >= 1
        if int(fields[0]) != 0:
            raise RuntimeError("Instrument returned error %s: %s" % (fields[0], fields[1]))

    def _validate_id(self) -> None:
        """Check the selected instrument is proper and responding.."""
        instrument_id = self._session.query("*IDN?")
        if not any(id_check in instrument_id for id_check in _SUPPORTED_INSTRUMENT_IDS):
            raise RuntimeError(
                "The ID query failed. This may mean that you selected the wrong instrument, your instrument did not respond, "
                f"or you are using a model that is not officially supported by this driver. Instrument ID: {instrument_id}"
            )

    def _reset(self) -> None:
        """Reset the instrument to a known state."""
        self._session.write("*CLS")
        self._session.write("*RST")
        self._check_error()


def build_visa_grpc_resource_string(
    resource_name: str,
    address: str,
    session_name: str = "",
    initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.AUTO,
) -> str:
    """Build an grpc:// resource string for remoting with NI-VISA."""
    query = {
        "init_behavior": _INITIALIZATION_BEHAVIOR[initialization_behavior],
        "session_name": session_name,
    }
    return f"grpc://{address}/{resource_name}?" + urlencode(query)


def get_visa_grpc_insecure_address(config: AutoConfig, discovery_client: DiscoveryClient) -> str:
    """Get the insecure address of NI gRPC Device Server's VISA interface in host:port format."""
    # Hack: config is a parameter for now so TestStand code modules use the right config path.
    use_grpc_device_server: bool = config(
        "MEASUREMENTLINK_USE_GRPC_DEVICE_SERVER", default=True, cast=bool
    )
    grpc_device_server_address: str = config(
        "MEASUREMENTLINK_GRPC_DEVICE_SERVER_ADDRESS", default=""
    )

    if not use_grpc_device_server:
        return ""

    if grpc_device_server_address:
        return urlsplit(grpc_device_server_address).netloc
    else:
        service_location = discovery_client.resolve_service(
            "visa_grpc.Visa", "ni.measurementlink.v1.grpcdeviceserver"
        )
        return service_location.insecure_address
