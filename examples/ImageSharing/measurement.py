"""A default measurement with an array in and out."""

import logging
import pathlib
import sys

import click
import ni_measurementlink_service as nims

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "ImageSharing.serviceconfig",
    version="1.0.0.0",
    ui_file_paths=[service_directory / "ImageSharing.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration("String in", nims.DataType.String, "data1.txt")
@measurement_service.configuration("path in", nims.DataType.Path, "data1.txt")
@measurement_service.output("String out", nims.DataType.String)
def measure(string_input, path_input):
    """TODO: replace the following line with your own measurement logic."""

    
    filePath = str(pathlib.Path.cwd()) + str('\\examples\\ImageSharing\\') + str(string_input)

    with open(filePath, 'r') as file:
        # Read the entire contents of the file into a string
        file_contents = file.read()
        print(file_contents)

    print('Measurement Completed.')

    string_output = file_contents
    return (string_output,)


@click.command
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging. Repeat to increase verbosity.",
)
def main(verbose: int) -> None:
    """Host the ImageSharing service."""
    if verbose > 1:
        level = logging.DEBUG
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)

    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
