from typing import Dict, List, Sequence

from ..motor import Motor
from .coordinatesystem import CoordinateSystem


class LinearTransform(CoordinateSystem):
    required_params: List[str] = [
        "cs_x_xscale",
        "cs_x_yscale",
        "cs_x_offset",
        "cs_y_xscale",
        "cs_y_yscale",
        "cs_y_offset",
    ]

    def __init__(
        self,
        name: str,
        cs_type: str,
        real_motor_mapping: Dict[str, str],
        cs_motor_mapping: Dict[str, str],
        motors: Sequence[Motor],
        cs_params: Dict[str, str] = None,
    ):
        self.check_cs_params(cs_params)
        super().__init__(
            name, cs_type, real_motor_mapping, cs_motor_mapping, motors, cs_params
        )

    def check_cs_params(self, cs_params) -> None:
        for param in self.required_params:
            if param not in cs_params:
                raise ValueError(f"Required parameter {param} is missing")

    def calculate_scaled_limit(
        self, raw_limit: float, scale_factor: float, offset: float
    ) -> float:
        return raw_limit * scale_factor + offset

    def update_cs_motor_attributes(self) -> None:
        """Called to update CS motor parameters
        - When the transform parameters are updated
        - When the real motor limits change
        - When the real motor velocities change
        - When the real motor accelerations change"""
        # Get properties of real motors
        real_motor_limits = self.get_real_motor_limit_values()

        # Get CS parameter values
        cs_param_values = self.get_cs_param_values()

        # Calculate what the CS X motor limit should be
        print(real_motor_limits)
        print(cs_param_values)

        cs_x_low_limit = min(
            self.calculate_scaled_limit(
                real_motor_limits["x"].low_limit,
                cs_param_values["cs_x_xscale"].value,
                cs_param_values["cs_x_offset"].value,
            ),
            self.calculate_scaled_limit(
                real_motor_limits["y"].low_limit,
                cs_param_values["cs_x_yscale"].value,
                cs_param_values["cs_x_offset"].value,
            ),
        )

        cs_x_high_limit = min(
            self.calculate_scaled_limit(
                real_motor_limits["x"].high_limit,
                cs_param_values["cs_x_xscale"].value,
                cs_param_values["cs_x_offset"].value,
            ),
            self.calculate_scaled_limit(
                real_motor_limits["y"].high_limit,
                cs_param_values["cs_x_yscale"].value,
                cs_param_values["cs_x_offset"].value,
            ),
        )

        cs_y_low_limit = min(
            self.calculate_scaled_limit(
                real_motor_limits["y"].low_limit,
                cs_param_values["cs_y_xscale"].value,
                cs_param_values["cs_y_offset"].value,
            ),
            self.calculate_scaled_limit(
                real_motor_limits["y"].low_limit,
                cs_param_values["cs_y_yscale"].value,
                cs_param_values["cs_y_offset"].value,
            ),
        )

        cs_y_high_limit = min(
            self.calculate_scaled_limit(
                real_motor_limits["y"].high_limit,
                cs_param_values["cs_y_xscale"].value,
                cs_param_values["cs_y_offset"].value,
            ),
            self.calculate_scaled_limit(
                real_motor_limits["y"].high_limit,
                cs_param_values["cs_y_yscale"].value,
                cs_param_values["cs_y_offset"].value,
            ),
        )

        print(f"CS X limits: {cs_x_low_limit} - {cs_x_high_limit}")
        print(f"CS Y limits: {cs_y_low_limit} - {cs_y_high_limit}")
