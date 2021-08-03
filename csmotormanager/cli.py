import logging
from argparse import ArgumentParser
from typing import List

from ruamel import yaml

from csmotormanager.config.config import get_logger, parse_config
from csmotormanager.cs.coordinatesystem import CoordinateSystem

from . import __version__

__all__ = ["main"]


def main(args=None):
    # Argument parsing
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("yaml", help="YAML configuration file")
    args = parser.parse_args(args)

    # Set up the logger
    get_logger()

    # Parse the input YAML
    coordinate_systems = []
    logging.info(f"Reading {args.yaml}")
    with open(args.yaml, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            coordinate_systems = parse_config(config)
        except yaml.YAMLError as exc:
            print(exc)

    # Run the IOC
    run_ioc(coordinate_systems)


def run_ioc(coordinate_systems: List[CoordinateSystem]):

    logging.info("Coordinate systems overview")
    for cs in coordinate_systems:
        print(cs.get_report_string())
        cs.update_cs_motor_attributes()
