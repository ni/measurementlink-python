"""Base class to reserve pins and create instrument object"""

import contextlib
import ni_measurementlink_service as nims


def InstrumentFal(instrument_type_id: str):
    """Create object based on the instrument type id."""    
    from Fal.DCPowerNI import DCPowerNI
    from Fal.DmmNI import DmmNI

    instrument = {
        "niDCPower": DCPowerNI,
        "niDMM": DmmNI,
    }

    return instrument[instrument_type_id]()


class Instrument():
    """Instrument base class."""

    @contextlib.contextmanager
    def initialize(measurement_service: nims.MeasurementService, pin_name: str):
        with measurement_service.context.reserve_session(pin_name) as reservation:
            instrument_obj = InstrumentFal(reservation.session_info.instrument_type_id)
            with instrument_obj.initialize(reservation, measurement_service) as _:
                yield instrument_obj