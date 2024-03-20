"""Base class to reserve pins and create Dmm object"""

import contextlib

import ni_measurementlink_service as nims


def DmmHal(instrument_type_id: str):
    """Create Dmm object based on the instrument type id."""    
    from dmm_hal.dmm_visa import DmmVisa
    from dmm_hal.dmm_ni import DmmNi

    dmm = {
        "niDMM": DmmNi,
        "VisaDmm": DmmVisa,
    }

    return dmm[instrument_type_id]()


class Dmm():
    """Multimeter base class."""

    @contextlib.contextmanager
    def initialize(measurement_service: nims.MeasurementService, pin_name: str):
        with measurement_service.context.reserve_session(pin_name) as reservation:
            dmm_hal_obj = DmmHal(reservation.session_info.instrument_type_id)
            with dmm_hal_obj.initialize(reservation) as _:
                yield dmm_hal_obj