import logging
from typing import Optional, Sequence, Union

from cothread.dbr import ca_array, ca_float, ca_int, ca_str

from .motor import Motor

# PV type for type hints
pv = Union[ca_array, ca_float, ca_int, ca_str]


def find_motor(name: str, motors: Sequence[Motor]) -> Optional[Motor]:
    for motor in motors:
        if motor.name == name:
            return motor
    return None


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
