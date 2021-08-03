import logging

from csmotormanager.cs.util import create_coordinate_system
from csmotormanager.motor.motor import Motor


def get_logger(
    date_format: str = "%d-%m-%Y %H:%M:%S", level_length: int = 7, name_length: int = 20
):
    format_string = (
        f"[%(asctime)s][%(levelname){level_length}s]"
        f"[%(name){name_length}s] %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_formatter = logging.Formatter(format_string, datefmt=date_format)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


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
            real_motor_mapping = entry[cs_key]["real_motors"]
            cs_motor_mapping = entry[cs_key]["cs_motors"]
            cs_params = entry[cs_key]["cs_params"]
            coordinate_systems.append(
                create_coordinate_system(
                    name,
                    cs_type,
                    real_motor_mapping,
                    cs_motor_mapping,
                    motors,
                    cs_params,
                )
            )
        else:
            raise ValueError(f"Unknown object: {entry}")

    logging.info(f"Found {len(coordinate_systems)} cs and {len(motors)} motors")
    return coordinate_systems
