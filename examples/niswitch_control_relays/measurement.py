"""Control relays using an NI relay driver (e.g. PXI-2567)."""

import contextlib
import logging
import pathlib
from typing import Tuple

import click
import niswitch
from _helpers import (
    ServiceOptions,
    configure_logging,
    get_service_options,
    grpc_device_options,
    use_simulation_option,
    verbosity_option,
)

import ni_measurementlink_service as nims

# To use a physical NI relay driver instrument, set this to False or specify
# --no-use-simulation on the command line.
USE_SIMULATION = True

service_directory = pathlib.Path(__file__).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "NISwitchControlRelays.serviceconfig",
    version="0.1.0.0",
    ui_file_paths=[service_directory / "NISwitchControlRelays.measui"],
)
service_options = ServiceOptions()


@measurement_service.register_measurement
@measurement_service.configuration("relay_names", nims.DataType.String, "SiteRelay1")
@measurement_service.configuration("close_relay", nims.DataType.Boolean, True)
def measure(
    relay_names: str,
    close_relays: bool,
) -> Tuple:
    """Control relays using an NI relay driver (e.g. PXI-2567)."""
    logging.info(
        "Controlling relays: relay_names=%s close_relay=%s",
        relay_names,
        close_relays,
    )

    session_management_client = nims.session_management.Client(
        grpc_channel=measurement_service.get_channel(
            provided_interface=nims.session_management.GRPC_SERVICE_INTERFACE_NAME,
            service_class=nims.session_management.GRPC_SERVICE_CLASS,
        )
    )

    with contextlib.ExitStack() as stack:
        relay_list = [r.strip() for r in relay_names.split(",")]
        reservation = stack.enter_context(
            session_management_client.reserve_sessions(
                context=measurement_service.context.pin_map_context,
                pin_or_relay_names=relay_list,
                instrument_type_id=nims.session_management.INSTRUMENT_TYPE_NI_RELAY_DRIVER,
                # If another measurement is using the session, wait for it to complete.
                # Specify a timeout to aid in debugging missed unreserve calls.
                # Long measurements may require a longer timeout.
                timeout=60,
            )
        )

        sessions = [
            stack.enter_context(_create_niswitch_session(session_info))
            for session_info in reservation.session_info
        ]

        for session, session_info in zip(sessions, reservation.session_info):
            session.relay_control(
                session_info.channel_list,
                niswitch.RelayAction.CLOSE if close_relays else niswitch.RelayAction.OPEN,
            )
        for session in sessions:
            session.wait_for_debounce()

    logging.info("Completed operation")
    return ()


def _create_niswitch_session(
    session_info: nims.session_management.SessionInformation,
) -> niswitch.Session:
    options = {}
    if service_options.use_simulation:
        options["simulate"] = True
        options["driver_setup"] = {"Model": "2567"}

    session_kwargs = {}
    if service_options.use_grpc_device:
        session_grpc_address = service_options.grpc_device_address

        if not session_grpc_address:
            session_grpc_channel = measurement_service.get_channel(
                provided_interface=niswitch.GRPC_SERVICE_INTERFACE_NAME,
                service_class="ni.measurementlink.v1.grpcdeviceserver",
            )
        else:
            session_grpc_channel = measurement_service.channel_pool.get_channel(
                target=session_grpc_address
            )
        session_kwargs["grpc_options"] = niswitch.GrpcSessionOptions(
            session_grpc_channel,
            session_name=session_info.session_name,
            initialization_behavior=niswitch.SessionInitializationBehavior.AUTO,
        )

    # This uses the topology configured in MAX.
    return niswitch.Session(session_info.resource_name, options=options, **session_kwargs)


@click.command
@verbosity_option
@grpc_device_options
@use_simulation_option(default=USE_SIMULATION)
def main(verbosity: int, **kwargs) -> None:
    """Control relays using an NI relay driver (e.g. PXI-2567)."""
    configure_logging(verbosity)
    global service_options
    service_options = get_service_options(**kwargs)

    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
