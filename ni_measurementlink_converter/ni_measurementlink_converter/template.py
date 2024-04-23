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


def _get_input_configurations(params):
    extracted_params = {}
    for param in params:
        parts = param.split(':')
        if len(parts) != 2:
            raise click.BadParameter(f"Invalid parameter format: {param}. Please use the format 'name:type'")
        name, param_type = parts
        if param_type == 'int':
            extracted_params[name] = 'nims.DataType.Int32'
        elif param_type == 'bool':
            extracted_params[name] = 'nims.DataType.Boolean'
        elif param_type == 'float':
            extracted_params[name] = 'nims.DataType.Double'
        elif param_type == 'List[float]':
            extracted_params[name] = 'nims.DataType.FloatArray1D'
        elif param_type == 'List[bool]':
            extracted_params[name] = 'nims.DataType.DoubleArray1D'
        else:
            raise click.BadParameter("Invalid parameter")
    return extracted_params


def _get_instrument(instrument_type):
    if instrument_type == "nidcpower":
        return 'nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER'
    else:
        raise click.BadParameter(f"Invalid instrument")
    

def _generate_method_signature(inputs):
    signature = ", ".join(inputs)
    return signature


def _get_parameter_string(inputs):
    parameter_names = [param.split(":")[0] for param in inputs]
    return ", ".join(parameter_names)


def _get_all_types(inputs):
    all_types = []
    for param in inputs:
        param_type = param.split(":")[1]
        all_types.append(param_type)
    return ", ".join(all_types)
    

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

    input_configurations = _get_input_configurations(inputs)
    output_configurations = _get_input_configurations(outputs)

    instrument = _get_instrument(instrument_type)
    input_signature = _generate_method_signature(inputs)
    input_param_names = _get_parameter_string(inputs)

    output_param_types = _get_all_types(outputs)

    service_class = f"{display_name}_Python"
    display_name_for_filenames = re.sub(r"\s+", "", display_name)
    serviceconfig_file = f"{display_name_for_filenames}.serviceconfig"
    directory_out_path = pathlib.Path.cwd() / display_name_for_filenames
    directory_out_path.mkdir(exist_ok=True, parents=True)
    measurement_version = 1.0

    source_file = "C:\\Users\\avinash.suresh\\Desktop\\Py utility\\Measurements\\Step2_Wrap.py"
    new_name = 'Meas.py'
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
        instrument=instrument,
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
