"""Helper classes and functions for MeasurementLink examples."""

import abc
import logging
import pathlib

from enum import Enum
from typing import Any, Callable, TypeVar

import click
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

class TestStandSupport(object):
    """Class that communicates with TestStand."""

    def __init__(self, sequence_context: Any) -> None:
        """Initialize the TestStandSupport object.

        Args:
            sequence_context:
                The SequenceContext COM object from the TestStand sequence execution.
                (Dynamically typed.)
        """
        self._sequence_context = sequence_context

    def get_active_pin_map_id(self) -> str:
        """Get the active pin map id from the NI.MeasurementLink.PinMapId runtime variable.

        Returns:
            The resource id of the pin map that is registered to the pin map service.
        """
        return self._sequence_context.Execution.RunTimeVariables.GetValString(
            "NI.MeasurementLink.PinMapId", 0x0
        )

    def resolve_file_path(self, file_path: str) -> str:
        """Resolve the absolute path to a file using the TestStand search directories.

        Args:
            file_path:
                An absolute or relative path to the file. If this is a relative path, this function
                searches the TestStand search directories for it.

        Returns:
            The absolute path to the file.
        """
        if pathlib.Path(file_path).is_absolute():
            return file_path
        (_, absolute_path, _, _, user_canceled) = self._sequence_context.Engine.FindFileEx(
            fileToFind=file_path,
            absolutePath=None,
            srchDirType=None,
            searchDirectoryIndex=None,
            userCancelled=None,  # Must match spelling used by TestStand
            searchContext=self._sequence_context.SequenceFile,
        )
        if user_canceled:
            raise RuntimeError("File lookup canceled by user.")
        return absolute_path
    

def configure_measurement_digits(session, measurement_type, range, resolution_digits):
     if INSTRUMENT_TYPE_VISA_DMM:
        session.configure_measurement_digits(measurement_type, range, resolution_digits)
     else:
        nidmm_function = nidmm.Function(measurement_type.value or Function.DC_VOLTS.value)
        session.configure_measurement_digits(measurement_type, range, resolution_digits)


def configure_logging(verbosity: int) -> None:
    """Configure logging for this process."""
    if verbosity > 1:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)


F = TypeVar("F", bound=Callable)


def verbosity_option(func: F) -> F:
    """Decorator for --verbose command line option."""
    return click.option(
        "-v",
        "--verbose",
        "verbosity",
        count=True,
        help="Enable verbose logging. Repeat to increase verbosity.",
    )(func)

# HAL Implementation starts here...
class HALSessionManager():
    pass

class DmmHAL(abc.ABC):
    @abc.abstractmethod
    def initialise(resource_name: str):
        pass

    @abc.abstractmethod
    def configure():
        pass

    @abc.abstractmethod
    def read():
        pass


class DmmHALNI(DmmHAL):
    def initialise(resource_name: str):
        pass

    def configure():
        pass

    def read():
        pass

class DmmHALVISA(DmmHAL):
    def initialise(resource_name: str):
        pass

    def configure():
        pass

    def read():
        pass