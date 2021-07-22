import pytest

from csmotormanager.cs.lineartransform import LinearTransform

from .util import MockMotor


class TestLinearTransform:
    # Attributes
    name = "KB mirrors"
    cs_type = "linear_transform"
    real_motor_mapping = {"x": "kb_x", "y": "kb_y"}
    cs_motor_mapping = {"x": "kb_cs_x", "y": "kb_cs_y"}
    motors = [
        MockMotor("kb_x", "MOTOR:X"),
        MockMotor("kb_y", "MOTOR:Y"),
        MockMotor("kb_cs_x", "MOTOR:CS:X"),
        MockMotor("kb_cs_y", "MOTOR:CS:Y"),
    ]
    cs_params = {
        "cs_x_xscale": "CS:X:XSCALE",
        "cs_x_yscale": "CS:X:YSCALE",
        "cs_x_offset": "CS:X:OFFSET",
        "cs_y_xscale": "CS:Y:XSCALE",
        "cs_y_yscale": "CS:Y:YSCALE",
        "cs_y_offset": "CS:Y:OFFSET",
    }

    @pytest.fixture(autouse=True)
    def setup_cs(self):
        # Create the coordinate system
        self.cs = LinearTransform(
            self.name,
            self.cs_type,
            self.real_motor_mapping,
            self.cs_motor_mapping,
            self.motors,
            self.cs_params,
        )

    def test_parameters_are_initialised(self):
        assert self.cs.name == self.name
        assert self.cs.cs_type == self.cs_type
        assert self.cs.cs_params == self.cs_params
        assert self.cs.real_motors["x"].name == "kb_x"
        assert self.cs.real_motors["y"].name == "kb_y"
        assert self.cs.cs_motors["x"].name == "kb_cs_x"
        assert self.cs.cs_motors["y"].name == "kb_cs_y"

    def test_check_cs_params_when_missing_required_parameter(self):
        required_params = list(self.cs_params)

        for index in range(len(required_params)):
            # Skip out parameter at index i
            params_with_missing_param = (
                required_params[0:index] + required_params[index + 1 :]
            )

            with pytest.raises(ValueError) as value_error:
                self.cs.check_cs_params(params_with_missing_param)

            assert (
                str(value_error.value)
                == f"Required parameter {required_params[index]} is missing"
            )
