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
