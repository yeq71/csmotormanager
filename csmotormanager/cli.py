import logging
from argparse import ArgumentParser
from typing import List

from ruamel import yaml

from . import __version__
from .cs.coordinatesystem import CoordinateSystem
from .cs.util import create_coordinate_system
from .motor import Motor
from .util import get_logger

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


def parse_config(config):
    logging.info("Parsing YAML")
    motors = []
    coordinate_systems = []
    motor_key = "motor"
    cs_key = "cs"
    for entry in config:
        if motor_key in entry:
            name = entry[motor_key]["name"]
            prefix = entry[motor_key]["prefix"]
            motors.append(Motor(name, prefix))
        elif cs_key in entry:
            name = entry[cs_key]["name"]
            cs_type = entry[cs_key]["type"]
            real_motors = entry[cs_key]["real_motors"]
            cs_motors = entry[cs_key]["cs_motors"]
            cs_params = entry[cs_key]["cs_params"]
            coordinate_systems.append(
                create_coordinate_system(
                    name, cs_type, real_motors, cs_motors, motors, cs_params
                )
            )
        else:
            raise ValueError(f"Unknown object: {entry}")

    logging.info(f"Found {len(coordinate_systems)} cs and {len(motors)} motors")
    return coordinate_systems


def run_ioc(coordinate_systems: List[CoordinateSystem]):

    logging.info("Coordinate systems overview")
    for cs in coordinate_systems:
        cs.report()
