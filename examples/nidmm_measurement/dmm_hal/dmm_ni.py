
from enum import Enum
from dmm_hal.dmm import Dmm
import nidmm


class Function(Enum):
    """Wrapper enum that contains a zero value."""

    NONE = 0
    DC_VOLTS = nidmm.Function.DC_VOLTS.value
    AC_VOLTS = nidmm.Function.AC_VOLTS.value
    DC_CURRENT = nidmm.Function.DC_CURRENT.value
    AC_CURRENT = nidmm.Function.AC_CURRENT.value
    TWO_WIRE_RES = nidmm.Function.TWO_WIRE_RES.value
    FOUR_WIRE_RES = nidmm.Function.FOUR_WIRE_RES.value
    FREQ = nidmm.Function.FREQ.value
    PERIOD = nidmm.Function.PERIOD.value
    TEMPERATURE = nidmm.Function.TEMPERATURE.value
    AC_VOLTS_DC_COUPLED = nidmm.Function.AC_VOLTS_DC_COUPLED.value
    DIODE = nidmm.Function.DIODE.value
    WAVEFORM_VOLTAGE = nidmm.Function.WAVEFORM_VOLTAGE.value
    WAVEFORM_CURRENT = nidmm.Function.WAVEFORM_CURRENT.value
    CAPACITANCE = nidmm.Function.CAPACITANCE.value
    INDUCTANCE = nidmm.Function.INDUCTANCE.value

    
class DmmNi(Dmm):
    """NI DMM Implementation"""
    def __init__(self, resource: str):
        """Constructor to create NI DMM reference"""
        self._session = nidmm.Session(resource)
    

    def configure_measurement_digits(self, measurement_function, range, resolution_digits):
        """Configures the common properties of the measurement. 
        
        These properties include method, range, and resolution_digits.
        """
        nidmm_function = nidmm.Function(measurement_function.value or Function.DC_VOLTS.value)
        self._session.configure_measurement_digits(nidmm_function, range, resolution_digits)

   
    def read(self):
        """Acquires a single measurement and returns the measured value."""
        self._session.read()