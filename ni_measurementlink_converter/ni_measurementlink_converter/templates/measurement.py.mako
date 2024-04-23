<%page args="display_name, version, service_class, serviceconfig_file,resource_name,instrument_type,instrument,input_configurations,output_configurations,input_signature,input_param_names,output_param_types"/>\
\
"""A default measurement with an array in and out."""

import logging
import pathlib
import sys
from typing import List, Tuple, Iterable
import ${instrument_type}
from Meas import measurement

import click
import ni_measurementlink_service as nims

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "${serviceconfig_file}",
    version="${version}",
    ui_file_paths=[service_directory / "test.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration(
    "pin_names",
    nims.DataType.IOResourceArray1D,
    ["${resource_name}"],
    instrument_type=${instrument},
)
    %for name, nims_type in input_configurations.items():
@measurement_service.configuration("${name}", ${nims_type})
    %endfor
    %for name, nims_type in output_configurations.items():
@measurement_service.output("${name}", ${nims_type})
    %endfor
def measure(pin_names: Iterable[str],${input_signature}) -> Tuple[${output_param_types}]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        with reservation.initialize_${instrument_type}_session() as session_info:
            return measurement(session_info.session, ${input_param_names})


def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
