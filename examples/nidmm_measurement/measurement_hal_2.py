

import logging
import pathlib
import sys
from typing import Tuple

import click
import ni_measurementlink_service as nims
import nidmm
from _helpers import configure_logging, verbosity_option, Function, configure_measurement_digits

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "NIDmmMeasurement.serviceconfig",
    version="0.1.0.0",
    ui_file_paths=[service_directory / "NIDmmMeasurement.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration(
    "pin_name",
    nims.DataType.Pin,
    "Pin1",
    instrument_type=nims.session_management.INSTRUMENT_TYPE_NI_DMM,
)
@measurement_service.configuration(
    "measurement_type", nims.DataType.Enum, Function.DC_VOLTS, enum_type=Function
)
@measurement_service.configuration(
    "instrument_type_id", str
) # Not the right way
@measurement_service.configuration("range", nims.DataType.Double, 10.0)
@measurement_service.configuration("resolution_digits", nims.DataType.Double, 5.5)
@measurement_service.output("measured_value", nims.DataType.Double)
def measure(
    pin_name: str,
    instrument_type_id: str,
    measurement_type: Function,
    range: float,
    resolution_digits: float,
) -> Tuple[float, bool, float]:
    """Perform a measurement using an NI DMM."""
    logging.info(
        "Starting measurement: pin_name=%s measurement_type=%s range=%g resolution_digits=%g",
        pin_name,
        measurement_type,
        range,
        resolution_digits,
    )

    with measurement_service.context.reserve_session(pin_name) as reservation:
        with reservation.initialize_session(measurement_service, instrument_type_id) as session_info:
            session = session_info.session
            configure_measurement_digits(session, measurement_type, range, resolution_digits)
            measured_value = session.read()
            # signal_out_of_range = math.isnan(measured_value) or math.isinf(measured_value)
            # absolute_resolution = session.resolution_absolute

    logging.info(
        "Completed measurement: measured_value=%g signal_out_of_range=%s absolute_resolution=%g",
        measured_value,
        # signal_out_of_range,
        # absolute_resolution,
    )
    return (measured_value,)


@click.command
@verbosity_option
def main(verbosity: int) -> None:
    """Perform a measurement using an NI DMM."""
    configure_logging(verbosity)

    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
