"""Base class to reserve pins and create instrument object"""

import contextlib
import importlib
import ni_measurementlink_service as nims


def _get_instrument(instrument_type):
    try:
        driver_module_path = f"Fal.{instrument_type}"
        driver_module = importlib.import_module(driver_module_path)
        return getattr(driver_module, instrument_type)
    except ImportError:
        raise ValueError(f"No driver found for instrument type '{instrument_type}'")


class Instrument():
    """Instrument base class."""

    @contextlib.contextmanager
    def initialize(measurement_service: nims.MeasurementService, pin_name: str):
        with measurement_service.context.reserve_session(pin_name) as reservation:
            instrument_obj = _get_instrument(reservation.session_info.instrument_type_id)()
            with instrument_obj.initialize_session(measurement_service, reservation, reservation.session_info.instrument_type_id) as _:
                yield instrument_obj