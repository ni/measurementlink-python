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

_logger = logging.getLogger(__name__)


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
    for input_param in inputs:
        name, input_type, default_value = input_param.split(':')
        input_type = _to_nims_type(input_type)
        input_data.append({'name': name, 'type': input_type, 'default_value': default_value})

    return input_data
    

def _extract_outputs(outputs):
    output_data = []
    for output_param in outputs:
        name, output_type = output_param.split(':')
        output_type = _to_nims_type(output_type)
        output_data.append({'name': name, 'type': output_type})

    return output_data


def _generate_method_signature(inputs):
    parameter_info = []
    for input_param in inputs:
        name, input_type, _ = input_param.split(':')
        parameter_info.append(f"{name}:{input_type}")

    return ", ".join(parameter_info)


def _get_input_names(inputs):
    parameter_names = [param.split(":")[0] for param in inputs]
    return ", ".join(parameter_names)


def _get_ouput_types(outputs):
    parameter_types = []
    for param in outputs:
        param_type = param.split(":")[1]
        parameter_types.append(param_type)
    return ", ".join(parameter_types)
    

@click.command()
@click.argument("display_name")
@click.option(
    "-r",
    "--resource_name",
    help="Resource name should be acted as pin name",
)
@click.option(
    "-t",
    "--instrument_type",
    help="Type of the instrument",
)
@click.option(
    "-i",
    "--inputs",
    help="Input parameter in the format name:type",
    multiple=True
)
@click.option(
    "-o",
    "--outputs",
    help="output parameter in the format name:type",
    multiple=True
)
def convert_measurement(
    display_name: str,
    resource_name: str,
    instrument_type: str,
    inputs: str,
    outputs: str,
) -> None:
    _logging(True)

    nims_instrument = _get_nims_instrument(instrument_type)

    input_configurations = _extract_inputs(inputs)
    output_configurations = _extract_outputs(outputs)

    input_signature = _generate_method_signature(inputs)
    input_param_names = _get_input_names(inputs)

    output_param_types = _get_ouput_types(outputs)

    service_class = f"{display_name}_Python"
    display_name_for_filenames = re.sub(r"\s+", "", display_name)
    serviceconfig_file = f"{display_name_for_filenames}.serviceconfig"
    directory_out_path = pathlib.Path.cwd() / display_name_for_filenames
    directory_out_path.mkdir(exist_ok=True, parents=True)
    measurement_version = 1.0

    source_file = "C:\\Users\\avinash.suresh\\Desktop\\Py utility\\Measurements\\dcpower_measurement.py"
    new_name = 'OldMeasurement.py'
    shutil.copy(str(source_file), str(directory_out_path) + str('\\') + new_name)

    _create_file(
        "measurement.py.mako",
        "measurement.py",
        directory_out_path,
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
        output_param_types=output_param_types
    )
    _create_file(
        "measurement.serviceconfig.mako",
        serviceconfig_file,
        directory_out_path,
        display_name=display_name,
        service_class=service_class,
    )
    _create_file("start.bat.mako", "start.bat", directory_out_path)
    _create_file("_helpers.py.mako", "_helpers.py", directory_out_path)
