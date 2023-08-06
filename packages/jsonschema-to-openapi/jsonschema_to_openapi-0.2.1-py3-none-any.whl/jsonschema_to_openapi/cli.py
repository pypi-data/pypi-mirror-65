"""
This module provides a cli tool for the package.
"""

import argparse

from jsonschema import Draft6Validator

from .convert import convert
from .utils import read_json, write_json, setup_logger


_LOGGER = setup_logger(__name__)


def _main(input_file, output_file):
    _LOGGER.info(f"Reading JSON schema from '{input_file}' ...")
    schema = read_json(input_file)
    _LOGGER.info("Validating JSON schema ...")
    Draft6Validator.check_schema(schema)
    _LOGGER.info("Converting JSON schema to OpenAPI specification ...")
    spec = convert(schema)
    _LOGGER.info(f"Writing OpenAPI specification to '{output_file}' ...")
    write_json(spec, output_file)
    _LOGGER.info("Done!")


def _parser():
    parser = argparse.ArgumentParser(
        description="Converts a JSON schema to an OpenAPI specification version 3.0.",
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="help", help="Shows help and exits the program."
    )

    parser.add_argument(
        "input_file", metavar="input-file", type=str, help="The JSON schema file."
    )

    parser.add_argument(
        "output_file",
        metavar="output-file",
        type=str,
        help="Where to store the OpenAPI specification.",
    )

    return parser


def main():
    """
    The main function for the cli.
    """
    parser = _parser()
    _main(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
