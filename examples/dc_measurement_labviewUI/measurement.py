"""User Measurement.

User can Import driver and 3rd Party Packages based on requirements.

"""

import logging
import os
import sys
import time

import click
import hightime
import nidcpower

import ni_measurement_service as nims


measurement_info = nims.MeasurementInfo(
    display_name="DCMeasurement(Py_VI)",
    version="0.1.0.0",
    measurement_type="DC",
    product_type="ADC",
    ui_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "DCMeasurementUI.vi"),
    ui_file_type=nims.UIFileType.LabVIEW,
)

service_info = nims.ServiceInfo(
    service_class="DCMeasurement_Python_VI",
    service_id="{B290B571-CB76-426F-9ACC-5168DC1B027B}",
    description_url="https://www.ni.com/measurementservices/dcmeasurement.html",
)
dc_measurement_service = nims.MeasurementService(measurement_info, service_info)


@dc_measurement_service.register_measurement
@dc_measurement_service.configuration("Resource name", nims.DataType.String, "DPS_4145")
@dc_measurement_service.configuration("Voltage level(V)", nims.DataType.Double, 6.0)
@dc_measurement_service.configuration("Voltage level range(V)", nims.DataType.Double, 6.0)
@dc_measurement_service.configuration("Current limit(A)", nims.DataType.Double, 0.01)
@dc_measurement_service.configuration("Current limit range(A)", nims.DataType.Double, 0.01)
@dc_measurement_service.configuration("Source delay(s)", nims.DataType.Double, 0.0)
@dc_measurement_service.output("Voltage Measurement(V)", nims.DataType.Double)
@dc_measurement_service.output("Current Measurement(A)", nims.DataType.Double)
def measure(
    resource_name,
    voltage_level,
    voltage_level_range,
    current_limit,
    current_limit_range,
    source_delay,
):
    """User Measurement API. Returns Voltage Measurement as the only output.

    Returns
    -------
        Tuple of Output Variables, in the order configured in the metadata.py

    """
    # User Logic :
    print("Executing DCMeasurement(Py)")

    def cancel_callback():
        print("Canceling DCMeasurement(Py)")
        if session is not None:
            nonlocal pending_cancellation
            pending_cancellation = True
            session.abort()

    pending_cancellation = False
    dc_measurement_service.context.add_cancel_callback(cancel_callback)
    time_remaining = dc_measurement_service.context.time_remaining()

    with nidcpower.Session(resource_name=resource_name) as session:
        # Configure the session.
        session.source_mode = nidcpower.SourceMode.SINGLE_POINT
        session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        session.current_limit = current_limit
        session.voltage_level_range = voltage_level_range
        session.current_limit_range = current_limit_range
        session.source_delay = hightime.timedelta(seconds=source_delay)
        session.voltage_level = voltage_level
        measured_voltage = None
        measured_current = None
        in_compliance = None
        with session.initiate():
            deadline = time.time() + time_remaining
            while deadline >= time.time():
                if pending_cancellation:
                    break
                try:
                    session.wait_for_event(nidcpower.enums.Event.SOURCE_COMPLETE, timeout=0.1)
                    break
                except nidcpower.DriverError as e:
                    """
                    There is no native way to support cancellation when taking a DCPower measurement.
                    To support cancellation, we will be calling WaitForEvent until it succeeds or
                    we have gone past the specified timeout. WaitForEvent will throw an exception
                    if it times out, which is why we are catching and doing nothing.
                    """
                    NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE = -1074116059
                    if e.code == NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE:
                        pass
                    else:
                        raise
            channel = session.get_channel_names("0")
            measured_voltage = session.channels[channel].measure(
                nidcpower.enums.MeasurementTypes.VOLTAGE
            )
            measured_current = session.channels[channel].measure(
                nidcpower.enums.MeasurementTypes.CURRENT
            )
            in_compliance = session.channels[channel].query_in_compliance()
        session = None  # Don't abort after this point

    print_fetched_measurements(measured_voltage, measured_current, in_compliance)
    print("---------------------------------")
    return (measured_voltage, measured_current)


def print_fetched_measurements(measured_voltage, measured_current, in_compliance):
    """Format and print the Measured Values."""
    layout = "{: >20} : {:f}{}"
    print("Fetched Measurement Values:")
    print(layout.format("Voltage", measured_voltage, " V"))
    print(layout.format("Current", measured_current, " A"))
    print(layout.format("In compliance", in_compliance, ""))


@click.command
@click.option(
    "-v", "--verbose", count=True, help="Enable verbose logging. Repeat to increase verbosity."
)
def main(verbose: int):
    """Host the DC Measurement (LabVIEW UI) service."""
    if verbose > 1:
        level = logging.DEBUG
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)

    dc_measurement_service.host_service()
    input("Press enter to close the measurement service.\n")
    dc_measurement_service.close_service()


if __name__ == "__main__":
    sys.exit(main())
