import contextlib
import grpc
import nidcpower
import threading
import time

from typing import List, NamedTuple
from contextlib import ExitStack
import ni_measurementlink_service as nims
from ni_measurementlink_service.session_management import (
    SingleSessionReservation,
)

    
_NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE = -1074116059
_NIDCPOWER_TIMEOUT_EXCEEDED_ERROR_CODE = -1074097933
_NIDCPOWER_TIMEOUT_ERROR_CODES = [
    _NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE,
    _NIDCPOWER_TIMEOUT_EXCEEDED_ERROR_CODE,
]


class _Measurement(NamedTuple):
    voltage: float
    current: float
    in_compliance: bool
    channel: str


class DCPowerNI():
    """NI DCPOWER Implementation"""

    @contextlib.contextmanager
    def initialize(self, reservation : SingleSessionReservation, measurement_service : nims.MeasurementService):    
        self.measurement_service = measurement_service
        with reservation.initialize_nidcpower_session() as session_info:
            self.session_info = session_info
            yield self.session_info


    def measure_dc_voltage(self, measurement_function, range, resolution_digits):
        """Configures the common properties of the measurement. 
        
        These properties include method, range, and resolution_digits.
        """
        channels = self.session_info.session.channels[self.session_info.channel_list]
        channels.source_mode = nidcpower.SourceMode.SINGLE_POINT
        channels.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        channels.voltage_level = range

        with ExitStack() as stack:
            channels = self.session_info.session.channels[self.session_info.channel_list]
            stack.enter_context(channels.initiate())

            # Wait for the outputs to settle.
            channels = self.session_info.session.channels[self.session_info.channel_list]
            timeout = 10.0
            cancellation_event = threading.Event()

            self._wait_for_event(
                channels, cancellation_event, nidcpower.enums.Event.SOURCE_COMPLETE, timeout
            )

            channels = self.session_info.session.channels[self.session_info.channel_list]
            session_measurements: List[_Measurement] = channels.measure_multiple()
            return session_measurements[0].voltage
    
        
    def _wait_for_event(
        self,
        channels: nidcpower.session._SessionBase,
        cancellation_event: threading.Event,
        event_id: nidcpower.enums.Event,
        timeout: float,
    ) -> None:
        """Wait for a NI-DCPower event or until error/cancellation occurs."""
        grpc_deadline = time.time() + self.measurement_service.context.time_remaining
        user_deadline = time.time() + timeout

        while True:
            if time.time() > user_deadline:
                raise TimeoutError("User timeout expired.")
            if time.time() > grpc_deadline:
                self.measurement_service.context.abort(
                    grpc.StatusCode.DEADLINE_EXCEEDED, "Deadline exceeded."
                )
            if cancellation_event.is_set():
                self.measurement_service.context.abort(
                    grpc.StatusCode.CANCELLED, "Client requested cancellation."
                )

            # Wait for the NI-DCPower event. If this takes more than 100 ms, check
            # whether the measurement was canceled and try again. NI-DCPower does
            # not support canceling a call to wait_for_event().
            try:
                channels.wait_for_event(event_id, timeout=100e-3)
                break
            except nidcpower.errors.DriverError as e:
                if e.code in _NIDCPOWER_TIMEOUT_ERROR_CODES:
                    pass
                raise
