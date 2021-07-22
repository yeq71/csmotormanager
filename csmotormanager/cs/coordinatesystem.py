from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import cothread.catools

from ..motor import Motor
from ..util import find_motor, pv


@dataclass
class MotorLimit:
    """Class for motor limit values"""

    name: str
    low_limit: float
    high_limit: float

    def __str__(self) -> str:
        return f"{self.name} limits: {self.low_limit}, {self.high_limit}"


@dataclass
class Parameter:
    """Parameter data class"""

    name: str
    value: float

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


class CoordinateSystem:
    def __init__(
        self,
        name: str,
        cs_type: str,
        real_motor_mapping: Dict[str, str],
        cs_motor_mapping: Dict[str, str],
        motors: Sequence[Motor],
        cs_params: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.cs_type = cs_type
        self.cs_params = cs_params
        self.real_motors: Dict[str, Motor] = {}
        self.cs_motors: Dict[str, Motor] = {}

        self.set_motors(real_motor_mapping, cs_motor_mapping, motors)

    def set_motors(
        self,
        real_motor_mapping: Dict[str, str],
        cs_motor_mapping: Dict[str, str],
        motors: Sequence[Motor],
    ):
        for axis, name in real_motor_mapping.items():
            motor = find_motor(name, motors)
            if not motor:
                raise ValueError(f"Real motor {name} not found for axis {axis}")
            self.real_motors[axis] = motor
        for axis, name in cs_motor_mapping.items():
            motor = find_motor(name, motors)
            if not motor:
                raise ValueError(f"CS motor {name} not found for CS axis {axis}")
            self.cs_motors[axis] = motor

    def get_cs_param_value(self, param_name: str) -> pv:
        if not self.cs_params:
            raise ValueError("No CS parameters defined")
        return cothread.catools.caget(f"{self.cs_params[param_name]}")

    def __str__(self) -> str:
        return (
            f"CS {self.name} ({self.cs_type}):\n"
            f"  Real motors: {self.real_motors}\n"
            f"  CS motors: {self.cs_motors}"
        )

    def report(self) -> None:
        report_string = f"{self.name} (type {self.cs_type})\n"
        report_string += "Real motors:\n"
        for _, motor in self.real_motors.items():
            report_string += f"  {motor.get_report_string()}\n"
        report_string += "\nCS motors:\n"
        for _, motor in self.cs_motors.items():
            report_string += f"  {motor.get_report_string()}\n"
        report_string += "\nCS parameters:\n"
        param_values = self.get_cs_param_values()
        for param in param_values:
            report_string += f"  {param.name}: {param.value:f}\n"
        print(report_string)

    def get_real_motor_limit_values(self) -> List[MotorLimit]:
        motor_limits = []
        for axis, motor in self.real_motors.items():
            low_limit, high_limit = motor.get_limits()
            motor_limits.append(MotorLimit(motor.name, low_limit, high_limit))
        return motor_limits

    def get_cs_param_values(self):
        params = []
        for param in self.cs_params:
            value = self.get_cs_param_value(param)
            params.append(Parameter(param, value))
        return params
