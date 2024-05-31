<%page args="display_name, version, service_class, serviceconfig_file,resource_name,instrument_type,nims_instrument,input_configurations,output_configurations,input_signature,input_param_names,output_param_types,updated_file_name,method_name"/>\
\
"""A default measurement with an array in and out."""

import logging
import pathlib
import sys
from typing import List, Tuple, Iterable
import ${instrument_type}
from ${updated_file_name} import ${method_name}

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
    nims.DataType.PinArray1D,
    ["${resource_name}"],
    instrument_type=${nims_instrument},
)
    %for input_config in input_configurations:
@measurement_service.configuration("${input_config['name']}", ${input_config['type']}, ${input_config['default_value']})
    %endfor
    %for output_config in output_configurations:
@measurement_service.output("${output_config['name']}", ${output_config['type']})
    %endfor
def measure(pin_names: Iterable[str], ${input_signature}) -> Tuple[${output_param_types}]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        return ${method_name}(reservation, ${input_param_names})


def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
