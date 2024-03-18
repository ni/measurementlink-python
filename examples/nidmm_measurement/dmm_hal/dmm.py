import contextlib
from dmm_hal import dmm_visa
from dmm_hal.dmm_ni import DmmNi

import ni_measurementlink_service as nims


def DmmHal(instrument_type_id: str):
    dmm = {
        "niDMM": DmmNi,
        "visadmm": dmm_visa,
    }

    return dmm[instrument_type_id]()


class Dmm():
    """Multimeter abstraction"""

    @contextlib.contextmanager
    def session_manager(measurement_service: nims.MeasurementService, pin_name: str):
        with measurement_service.context.reserve_session(pin_name) as reservation:
            dmm_hal_obj = DmmHal(reservation.session_info.instrument_type_id)
            yield (dmm_hal_obj, reservation)
