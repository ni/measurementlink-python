import pathlib
from typing import Generator, Iterable, NamedTuple

import pytest

from ni_measurementlink_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    MeasureRequest,
)
from ni_measurementlink_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2_grpc import (
    MeasurementServiceStub,
)
from ni_measurementlink_service._internal.stubs.ni.measurementlink.pin_map_context_pb2 import (
    PinMapContext,
)
from ni_measurementlink_service.measurement.service import MeasurementService
from tests.assets.nidcpower_measurement_pb2 import NIDCPowerConfigurations, NIDCPowerOutputs
from tests.utilities import nidcpower_measurement
from tests.utilities.pin_map_client import PinMapClient

_SITE = 0


def test___single_session___measure___measured_values_returned(
    pin_map_context: PinMapContext,
    stub_v2: MeasurementServiceStub,
) -> None:
    pin_names = ["Pin1"]
    configurations = NIDCPowerConfigurations(pin_names=pin_names, current_limit=0.01)

    outputs = _measure(stub_v2, pin_map_context, configurations)

    assert outputs.voltage_measurements == [5]
    assert outputs.current_measurements == [0.0001]


def test___single_session___measure___single_session_created(
    pin_map_context: PinMapContext,
    stub_v2: MeasurementServiceStub,
) -> None:
    pin_names = ["Pin1"]
    configurations = NIDCPowerConfigurations(pin_names=pin_names, current_limit=0.01)

    outputs = _measure(stub_v2, pin_map_context, configurations)

    assert _get_output(outputs) == [
        _MeasurementOutput("DCPower1/0", "DCPower1/0", "DCPower1/0", "DCPower1/0")
    ]


def test___multiple_sessions___measure___multiple_sessions_created(
    pin_map_context: PinMapContext,
    stub_v2: MeasurementServiceStub,
) -> None:
    pin_names = ["Pin1", "Pin2"]
    configurations = NIDCPowerConfigurations(
        pin_names=pin_names, current_limit=0.01, multi_session=True
    )

    outputs = _measure(stub_v2, pin_map_context, configurations)

    assert _get_output(outputs) == [
        _MeasurementOutput("DCPower1/0", "DCPower1/0", "DCPower1/0", "DCPower1/0"),
        _MeasurementOutput("DCPower1/2", "DCPower1/2", "DCPower1/2", "DCPower1/2"),
    ]


def _measure(
    stub_v2: MeasurementServiceStub,
    pin_map_context: PinMapContext,
    configurations: NIDCPowerConfigurations,
) -> NIDCPowerOutputs:
    request = MeasureRequest(pin_map_context=pin_map_context)
    request.configuration_parameters.Pack(configurations)
    response_iterator = stub_v2.Measure(request)
    responses = list(response_iterator)
    assert len(responses) == 1
    outputs = NIDCPowerOutputs.FromString(responses[0].outputs.value)
    return outputs


@pytest.fixture(scope="module")
def measurement_service() -> Generator[MeasurementService, None, None]:
    """Test fixture that creates and hosts a measurement service."""
    with nidcpower_measurement.measurement_service.host_service() as service:
        yield service


@pytest.fixture
def pin_map_context(pin_map_client: PinMapClient, pin_map_directory: pathlib.Path) -> PinMapContext:
    pin_map_name = "1Smu2ChannelGroup2Pin1Site.pinmap"
    pin_map_id = pin_map_client.update_pin_map(pin_map_directory / pin_map_name)

    return PinMapContext(pin_map_id=pin_map_id, sites=[_SITE])


class _MeasurementOutput(NamedTuple):
    session_name: str
    resource_name: str
    channel_list: str
    connected_channels: str


def _get_output(outputs: NIDCPowerOutputs) -> Iterable[_MeasurementOutput]:
    measurement_output = []
    for session_name, resource_name, channel_list, connected_channels in zip(
        outputs.session_names,
        outputs.resource_names,
        outputs.channel_lists,
        outputs.connected_channels,
    ):
        measurement_output.append(
            _MeasurementOutput(session_name, resource_name, channel_list, connected_channels)
        )

    return measurement_output
