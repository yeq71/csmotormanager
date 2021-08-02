from dataclasses import dataclass
from typing import Dict, Optional, Sequence

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
    """Base class to be overridden with an actual CS type"""

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

    def get_cs_param_values(self) -> Dict[str, Parameter]:
        params = {}
        if self.cs_params:
            for name, _ in self.cs_params.items():
                value = self.get_cs_param_value(name)
                params[name] = Parameter(name, value)
        return params

    def __str__(self) -> str:
        return (
            f"CS {self.name} ({self.cs_type}):\n"
            f"  Real motors: {self.real_motors}\n"
            f"  CS motors: {self.cs_motors}"
        )

    def get_report_string(self) -> str:
        report_string = f"{self.name} ({self.cs_type})\n"
        report_string += "Real motors:\n"
        for _, motor in self.real_motors.items():
            report_string += f"  {motor.get_report_string()}\n"
        report_string += "\nCS motors:\n"
        for _, motor in self.cs_motors.items():
            report_string += f"  {motor.get_report_string()}\n"
        report_string += "\nCS parameters:\n"
        param_values = self.get_cs_param_values()
        for name, param in param_values.items():
            report_string += f"  {name}: {param.value:f}\n"
        return report_string

    def get_real_motor_limit_values(self) -> Dict[str, MotorLimit]:
        motor_limits = {}
        for axis, motor in self.real_motors.items():
            low_limit, high_limit = motor.get_limits()
            motor_limits[axis] = MotorLimit(motor.name, low_limit, high_limit)
        return motor_limits

    def update_cs_motor_attributes(self):
        """This should be called to update CS motor parameters"""
        raise NotImplementedError("Override this method in subclass")
