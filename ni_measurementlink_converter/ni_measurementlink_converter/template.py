"""Utilizes command line args to create a measurement using template files."""

import logging
import pathlib
import re
from typing import Any, Optional, Tuple

import click
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


@click.command()
@click.argument("display_name")
def convert_measurement(
    display_name: str,
) -> None:
    _logging(True)

    service_class = f"{display_name}_Python"
    display_name_for_filenames = re.sub(r"\s+", "", display_name)
    serviceconfig_file = f"{display_name_for_filenames}.serviceconfig"
    directory_out_path = pathlib.Path.cwd() / display_name_for_filenames
    directory_out_path.mkdir(exist_ok=True, parents=True)
    measurement_version = 1.0

    _create_file(
        "measurement.py.mako",
        "measurement.py",
        directory_out_path,
        display_name=display_name,
        version=measurement_version,
        service_class=service_class,
        serviceconfig_file=serviceconfig_file,
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
