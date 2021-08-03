from typing import Dict, List, Optional

from csmotormanager.motor.motor import Motor

from .lineartransform import LinearTransform


def create_coordinate_system(
    name: str,
    cs_type: str,
    real_motor_mapping: Dict[str, str],
    cs_motor_mapping: Dict[str, str],
    motors: List[Motor],
    cs_params: Optional[Dict[str, str]],
):
    if cs_type == "linear_transform":
        return LinearTransform(
            name, cs_type, real_motor_mapping, cs_motor_mapping, motors, cs_params
        )
    else:
        raise ValueError(f"Unknown coordinate system {cs_type}")
