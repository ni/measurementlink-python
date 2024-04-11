from __future__ import annotations

import contextlib
import pathlib

import ni_measurementlink_service as nims
from dmm_hal._visa_dmm_session_management import VisaDmmSessionConstructor
from dmm_hal._visa_dmm import Function, INSTRUMENT_TYPE_VISA_DMM

from decouple import AutoConfig

# Search for the `.env` file starting with the current directory.
_config = AutoConfig(str(pathlib.Path.cwd()))


class DmmVisa():
    """An NI-VISA DMM Implementation."""
    @contextlib.contextmanager
    def initialize(self, reservation, measurement_service: nims.MeasurementService):
        """Initialize a single NI-VISA DMM instrument session."""
        session_constructor = VisaDmmSessionConstructor(_config, measurement_service.discovery_client)

        with reservation.initialize_session(
            session_constructor, INSTRUMENT_TYPE_VISA_DMM
        ) as session_info:            
            self._session = session_info.session
            yield self._session


    def configure_measurement_digits(self, measurement_function, range, resolution_digits):
        """Configures the common properties of the measurement. 
        
        These properties include method, range, and resolution_digits.
        """
        visa_dmm_function = Function(measurement_function.value)

        self._session.configure_measurement_digits(visa_dmm_function, range, resolution_digits)

   
    def read(self):
        """Acquires a single measurement and returns the measured value."""
        return self._session.read()
