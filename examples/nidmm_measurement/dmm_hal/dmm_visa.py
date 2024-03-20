import contextlib
import pathlib

import ni_measurementlink_service as nims
from decouple import AutoConfig

# Search for the `.env` file starting with the current directory.
_config = AutoConfig(str(pathlib.Path.cwd()))

class DmmVisa():
    """An NI-VISA DMM Implementation."""
    @contextlib.contextmanager
    def initialize(self, reservation_obj):
        """Initialize a single NI-VISA DMM instrument session."""
        with reservation_obj.initialize_session(
            session_constructor, INSTRUMENT_TYPE_VISA_DMM
        ) as session_info:            
            self._session = session_info.session
            yield self._session


    def configure_measurement_digits(self, measurement_function, range, resolution_digits):
        """Configures the common properties of the measurement. 
        
        These properties include method, range, and resolution_digits.
        """
        self._session.configure_measurement_digits(measurement_function, range, resolution_digits)

   
    def read(self):
        """Acquires a single measurement and returns the measured value."""
        self._session.read()