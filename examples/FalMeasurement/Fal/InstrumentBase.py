import abc
import contextlib
import functools
import importlib

import ni_measurementlink_service as nims

from ni_measurementlink_service.session_management._constants import (
    INSTRUMENT_TYPE_NI_DCPOWER,
    INSTRUMENT_TYPE_NI_HSDIO,
    INSTRUMENT_TYPE_NI_RFSA,
    INSTRUMENT_TYPE_NI_RFMX,
    INSTRUMENT_TYPE_NI_RFSG,
    INSTRUMENT_TYPE_NI_RFPM,
    INSTRUMENT_TYPE_NI_DMM,
    INSTRUMENT_TYPE_NI_DIGITAL_PATTERN,
    INSTRUMENT_TYPE_NI_SCOPE,
    INSTRUMENT_TYPE_NI_FGEN,
    INSTRUMENT_TYPE_NI_DAQMX,
    INSTRUMENT_TYPE_NI_RELAY_DRIVER,
    INSTRUMENT_TYPE_NI_MODEL_BASED_INSTRUMENT,
    INSTRUMENT_TYPE_NI_SWITCH_EXECUTIVE_VIRTUAL_DEVICE,
)
from ni_measurementlink_service.session_management._types import (
    SessionInformation,
    SessionInitializationBehavior,
    TSession,
    TypedSessionInformation,
)
from ni_measurementlink_service.session_management import (
    SingleSessionReservation,
)
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Optional,
)
from ni_measurementlink_service._drivers import (
    closing_session_with_ts_code_module_support,
)


supported_instruments = {
    INSTRUMENT_TYPE_NI_DCPOWER,
    INSTRUMENT_TYPE_NI_HSDIO,
    INSTRUMENT_TYPE_NI_RFSA,
    INSTRUMENT_TYPE_NI_RFMX,
    INSTRUMENT_TYPE_NI_RFSG,
    INSTRUMENT_TYPE_NI_RFPM,
    INSTRUMENT_TYPE_NI_DMM,
    INSTRUMENT_TYPE_NI_DIGITAL_PATTERN,
    INSTRUMENT_TYPE_NI_SCOPE,
    INSTRUMENT_TYPE_NI_FGEN,
    INSTRUMENT_TYPE_NI_DAQMX,
    INSTRUMENT_TYPE_NI_RELAY_DRIVER,
    INSTRUMENT_TYPE_NI_MODEL_BASED_INSTRUMENT,
    INSTRUMENT_TYPE_NI_SWITCH_EXECUTIVE_VIRTUAL_DEVICE,
}

def _is_supported_instrument(instrument_type:str) -> bool:
    if instrument_type in supported_instruments:
        return True
    return False


def _get_session_constructor(instrument_type: str, is_supported_instrument: bool) -> Callable[[SessionInformation], TSession]:
    if is_supported_instrument:
        try:
            driver_module_name = f"ni_measurementlink_service._drivers._{instrument_type.lower()}"  # Assuming drivers are in a package named 'drivers'
            driver_module = importlib.import_module(driver_module_name)
            return driver_module.SessionConstructor
        except ImportError:
            raise ValueError(f"No driver found for instrument type '{instrument_type}'")
    else:
        try:
            driver_module_path = f"Fal.{instrument_type}"
            driver_module = importlib.import_module(driver_module_path)
            return getattr(driver_module, instrument_type + 'Constructor')
        except ImportError:
            raise ValueError(f"No driver found for instrument type '{instrument_type}'")


class InstrumentBase():
    @contextlib.contextmanager
    def initialize_session(
        self,
        measurement_service: nims.MeasurementService,
        reservation = SingleSessionReservation,
        instrument_type = str,
        reset: bool = False,
        options: Optional[Dict[str, Any]] = None,
        initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.AUTO,
    ) -> Generator[TypedSessionInformation[TSession], None, None]:
        self.measurement_service = measurement_service
        session_constructor = None
        closing_function = None

        if(_is_supported_instrument(instrument_type)):
            session_constructor_object = _get_session_constructor(instrument_type, True)
            session_constructor = session_constructor_object(
                reservation._discovery_client, reservation._grpc_channel_pool, reset, options, initialization_behavior
            )

            closing_function = functools.partial(
                closing_session_with_ts_code_module_support, initialization_behavior
            )
        else:
            session_constructor_object = _get_session_constructor(instrument_type, False)
            session_constructor = session_constructor_object(
                measurement_service, initialization_behavior
            )

        with reservation._initialize_session_core(
            session_constructor, instrument_type, closing_function
        ) as session_info:
            self.session_info = session_info
            yield self.session_info