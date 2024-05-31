"""Utilizes command line args to create a measurement using template files."""

import logging
import pathlib
import re
from typing import Any
import shutil

import click
from pathlib import Path
from mako import exceptions
from mako.template import Template
import os
from ni_measurementlink_converter.helpers.Extract_inputs import extract_input_details
from ni_measurementlink_converter.helpers.Extract_outputs import get_return_details
from ni_measurementlink_converter.helpers.ModifyInputArgs import add_parameter_to_method
from ni_measurementlink_converter.helpers.ModifyInitialize import replace_session_initialization
from ni_measurementlink_converter.helpers.Assign_session import insert_session_assigning

_logger = logging.getLogger(__name__)
_drivers = [ 'nidcpower', 'nidmm' ]
instrument_type = ''
resource_name = ''
actual_session_name = ''


def _render_template(template_name: str, **template_args: Any) -> bytes:
    file_path = str(pathlib.Path(__file__).parent / "templates" / template_name)

    template = Template(filename=file_path, input_encoding="utf-8", output_encoding="utf-8")
    try:
        return template.render(**template_args)
    except Exception as e:
        _logger.error(exceptions.text_error_template().render())
        raise click.ClickException(
            f'An error occurred while rendering template "{template_name}".'
        ) from e


def _create_file(
    template_name: str, file_name: str, directory_out: pathlib.Path, **template_args: Any
) -> None:
    output_file = directory_out / file_name

    output = _render_template(template_name, **template_args)

    with output_file.open("wb") as fout:
        fout.write(output)


def _logging(verbose:bool):
    if verbose > 1:
        level = logging.DEBUG
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)


def _to_nims_type(type):
    if type == 'int':
        return 'nims.DataType.Int32'
    elif type == 'bool':
        return 'nims.DataType.Boolean'
    elif type == 'float':
        return 'nims.DataType.Double'
    elif type == 'List[float]':
        return 'nims.DataType.FloatArray1D'
    elif type == 'List[bool]':
        return 'nims.DataType.DoubleArray1D'
    else:
        raise click.BadParameter("Invalid parameter")


def _get_nims_instrument(instrument_type):
    if instrument_type == "nidcpower":
        return 'nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER'
    else:
        raise click.BadParameter(f"Invalid instrument")
    

def _extract_inputs(inputs):
    input_data = []
    
    for param_name, param_info in inputs.items():
        input_type = _to_nims_type(param_info['type'])
        input_data.append({'name': param_name, 'actual_type' : param_info['type'], 'type': input_type, 'default_value': param_info['default']})

    return input_data
    

def _extract_outputs(output_variable_names, output_return_types):
    output_data = []
    for var_name, return_type in zip(output_variable_names, output_return_types):
        output_type = _to_nims_type(return_type)
        output_data.append({'name': var_name, 'actual_type': return_type , 'type': output_type})

    return output_data


def _generate_method_signature(inputs):
    parameter_info = []
    for input_param in inputs:
        parameter_info.append(f"{input_param['name']}:{input_param['actual_type']}")

    return ", ".join(parameter_info)


def _get_input_names(inputs):
    parameter_names = [param['name'] for param in inputs]
    return ", ".join(parameter_names)


def _get_ouput_types(outputs):
    parameter_types = []
    for param in outputs:
        parameter_types.append(param['actual_type'])
    return ", ".join(parameter_types)
    

@click.command()
@click.argument("display_name")
@click.option(
    "-f",
    "--file_name",
    help="Name of the Measurement file",
)
@click.option(
    "-m",
    "--method_name",
    help="Name of the Measurement method",
)
def convert_measurement(
    display_name: str,
    file_name: str,
    method_name: str,
) -> None:
    _logging(True)

    current_directory = pathlib.Path.cwd()

    filename_without_extension, file_extension = os.path.splitext(file_name)
    updated_file_name = f"{filename_without_extension}_migrated{file_extension}"

    existing_measurement_path = str(current_directory) + str('\\') + file_name
    migrated_measurement_path = str(current_directory) + str('\\') + updated_file_name

    shutil.copy(existing_measurement_path, migrated_measurement_path)

    input_parameters = extract_input_details(existing_measurement_path, method_name)
    output_variable_names, output_variable_types = get_return_details(existing_measurement_path, method_name)

    input_configurations = _extract_inputs(input_parameters)

    output_configurations = _extract_outputs(output_variable_names, output_variable_types)


    input_signature = _generate_method_signature(input_configurations)

    input_param_names = _get_input_names(input_configurations)

    output_param_types = _get_ouput_types(output_configurations)

    add_parameter_to_method(migrated_measurement_path, method_name, 'reservation')
    session_details = replace_session_initialization(migrated_measurement_path, method_name, _drivers)
    for driver_name, param_value, actual_name in session_details:
        instrument_type = driver_name
        resource_name = param_value
        actual_session_name = actual_name
    insert_session_assigning(migrated_measurement_path, method_name, actual_session_name + " = session_info.session")

    nims_instrument = _get_nims_instrument(instrument_type)

    service_class = f"{display_name}_Python"
    display_name_for_filenames = re.sub(r"\s+", "", display_name)
    serviceconfig_file = f"{display_name_for_filenames}.serviceconfig"
    # directory_out_path.mkdir(exist_ok=True, parents=True)
    measurement_version = 1.0

    _create_file(
        "measurement.py.mako",
        "measurement.py",
        current_directory,
        display_name=display_name,
        version=measurement_version,
        service_class=service_class,
        serviceconfig_file=serviceconfig_file,
        resource_name=resource_name,
        instrument_type=instrument_type,
        nims_instrument=nims_instrument,
        input_configurations=input_configurations,
        output_configurations=output_configurations,
        input_signature = input_signature,
        input_param_names=input_param_names,
        output_param_types=output_param_types,
        updated_file_name=f"{filename_without_extension}_migrated",
        method_name=method_name
    )
    _create_file(
        "measurement.serviceconfig.mako",
        serviceconfig_file,
        current_directory,
        display_name=display_name,
        service_class=service_class,
    )
    _create_file("start.bat.mako", "start.bat", current_directory)
    _create_file("_helpers.py.mako", "_helpers.py", current_directory)
