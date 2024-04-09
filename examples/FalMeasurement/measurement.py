import pathlib
import sys

import nidmm
import ni_measurementlink_service as nims
from Fal.Instrument import Instrument 
from enum import Enum

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "FalMeasurement.serviceconfig",
    version="1.0.0.0",
    ui_file_paths=[service_directory / "FalMeasurement.measui"],
)


class Function(Enum):
    """Wrapper enum that contains a zero value."""

    NONE = 0
    DC_VOLTS = nidmm.Function.DC_VOLTS.value
    AC_VOLTS = nidmm.Function.AC_VOLTS.value
    DC_CURRENT = nidmm.Function.DC_CURRENT.value
    AC_CURRENT = nidmm.Function.AC_CURRENT.value
    TWO_WIRE_RES = nidmm.Function.TWO_WIRE_RES.value
    FOUR_WIRE_RES = nidmm.Function.FOUR_WIRE_RES.value
    FREQ = nidmm.Function.FREQ.value
    PERIOD = nidmm.Function.PERIOD.value
    TEMPERATURE = nidmm.Function.TEMPERATURE.value
    AC_VOLTS_DC_COUPLED = nidmm.Function.AC_VOLTS_DC_COUPLED.value
    DIODE = nidmm.Function.DIODE.value
    WAVEFORM_VOLTAGE = nidmm.Function.WAVEFORM_VOLTAGE.value
    WAVEFORM_CURRENT = nidmm.Function.WAVEFORM_CURRENT.value
    CAPACITANCE = nidmm.Function.CAPACITANCE.value
    INDUCTANCE = nidmm.Function.INDUCTANCE.value


@measurement_service.register_measurement
@measurement_service.configuration(
    "pin_name",
    nims.DataType.Pin,
    "Pin1",
)
@measurement_service.configuration(
    "measurement_type", nims.DataType.Enum, Function.DC_VOLTS, enum_type=Function
)
@measurement_service.configuration("range", nims.DataType.Double, 10.0)
@measurement_service.configuration("resolution_digits", nims.DataType.Double, 5.5)
@measurement_service.output("measured_value", nims.DataType.Double)
def measure(
    pin_name: str,
    measurement_type: Function,
    range: float,
    resolution_digits: float,
) -> float:
    with Instrument.initialize(measurement_service=measurement_service, pin_name=pin_name) as instrument:
        measured_value = instrument.measure_dc_voltage(measurement_type, range, resolution_digits)

    return (measured_value,)


def main() -> None:
    """Host the FalMeasurement service."""
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()