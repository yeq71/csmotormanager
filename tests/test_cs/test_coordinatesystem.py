from unittest.mock import patch

import pytest

from csmotormanager.cs.coordinatesystem import CoordinateSystem, MotorLimit, Parameter

from .util import MockMotor


def test_MotorLimit():
    name = "x_motor"
    low_limit = 5.3
    high_limit = 25.9

    motor_limit = MotorLimit(name, low_limit, high_limit)

    assert motor_limit.name == name
    assert motor_limit.low_limit == low_limit
    assert motor_limit.high_limit == high_limit

    string = motor_limit.__str__()

    assert string == "x_motor limits: 5.3, 25.9"


def test_Parameter():
    name = "XY_skew"
    value = 0.985

    param = Parameter(name, value)

    assert param.name == name
    assert param.value == value

    string = param.__str__()

    assert string == "XY_skew: 0.985"


class TestCoordinateSystem:
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
        self.cs = CoordinateSystem(
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

    def test_set_motors_raises_ValueError_for_missing_real_motor(self):
        motors_missing_kb_x = [
            MockMotor("kb_y", "MOTOR:Y"),
            MockMotor("kb_cs_x", "MOTOR:CS:X"),
            MockMotor("kb_cs_y", "MOTOR:CS:Y"),
        ]

        with pytest.raises(ValueError) as value_error:
            self.cs.set_motors(
                self.real_motor_mapping, self.cs_motor_mapping, motors_missing_kb_x
            )

        assert str(value_error.value) == "Real motor kb_x not found for axis x"

    def test_set_motors_raises_ValueError_for_missing_cs_motor(self):
        motors_missing_kb_cs_y = [
            MockMotor("kb_x", "MOTOR:Y"),
            MockMotor("kb_y", "MOTOR:Y"),
            MockMotor("kb_cs_x", "MOTOR:CS:X"),
        ]

        with pytest.raises(ValueError) as value_error:
            self.cs.set_motors(
                self.real_motor_mapping, self.cs_motor_mapping, motors_missing_kb_cs_y
            )

        assert str(value_error.value) == "CS motor kb_cs_y not found for CS axis y"

    def test_string_representation(self):
        string = str(self.cs)

        assert string == (
            f"CS {self.cs.name} ({self.cs.cs_type}):\n"
            f"  Real motors: {self.cs.real_motors}\n"
            f"  CS motors: {self.cs.cs_motors}"
        )

    @patch("cothread.catools.caget")
    def test_get_cs_param_value(self, mock_caget):
        mock_caget.return_value = 15.0

        value = self.cs.get_cs_param_value("cs_x_xscale")

        mock_caget.assert_called_once_with("CS:X:XSCALE")
        assert value == 15.0

    def test_get_cs_param_value_raises_ValueError_for_no_params(self):
        # First delete the list of parameters
        self.cs.cs_params = None

        with pytest.raises(ValueError) as value_error:
            self.cs.get_cs_param_value("None-existent-param")

        assert str(value_error.value) == "No CS parameters defined"

    @patch("cothread.catools.caget")
    def test_get_cs_param_values(self, mock_caget):
        expected_values = [1, 2, 3, 4, 5, 6]
        expected_names = list(self.cs_params)

        mock_caget.side_effect = expected_values

        params = self.cs.get_cs_param_values()

        param_index = 0
        for name, param in params.items():
            assert name == expected_names[param_index]
            assert param.name == expected_names[param_index]
            assert param.value == expected_values[param_index]
            param_index += 1

    def test_update_cs_motor_attributes_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError) as not_implemented_error:
            self.cs.update_cs_motor_attributes()

        assert str(not_implemented_error.value) == "Override this method in subclass"

    @patch("cothread.catools.caget")
    def test_get_report_string(self, mock_caget):
        expected_values = [1, 2, 3, 4, 5, 6]
        mock_caget.side_effect = expected_values

        expected_report_string = (
            "KB mirrors (linear_transform)\n"
            "Real motors:\n"
            "  kb_x: 5.500000mm [-10.0, 10.0]\n"
            "  kb_y: 5.500000mm [-10.0, 10.0]\n"
            "\n"
            "CS motors:\n"
            "  kb_cs_x: 5.500000mm [-10.0, 10.0]\n"
            "  kb_cs_y: 5.500000mm [-10.0, 10.0]\n"
            "\n"
            "CS parameters:\n"
            "  cs_x_xscale: 1.000000\n"
            "  cs_x_yscale: 2.000000\n"
            "  cs_x_offset: 3.000000\n"
            "  cs_y_xscale: 4.000000\n"
            "  cs_y_yscale: 5.000000\n"
            "  cs_y_offset: 6.000000\n"
        )

        assert self.cs.get_report_string() == expected_report_string
