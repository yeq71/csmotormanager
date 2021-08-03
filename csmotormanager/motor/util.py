from dataclasses import dataclass
from typing import Optional, Sequence

from .motor import Motor


@dataclass
class MotorLimit:
    """Class for motor limit values"""

    name: str
    low_limit: float
    high_limit: float

    def __str__(self) -> str:
        return f"{self.name} limits: {self.low_limit}, {self.high_limit}"


def find_motor(name: str, motors: Sequence[Motor]) -> Optional[Motor]:
    for motor in motors:
        if motor.name == name:
            return motor
    return None
