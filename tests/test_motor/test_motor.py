from unittest.mock import patch

from csmotormanager.motor.motor import Motor


@patch("csmotormanager.motor.motor.Motor.get_pv")
def test_motor_init(mock_get_pv):
    name = "x_motor"
    prefix = "MO-MOTORS-01:X"
    units = "um"

    # Set the patched method's return value
    mock_get_pv.return_value = units

    motor = Motor(name, prefix)

    assert motor.name == name
    assert motor.prefix == prefix
    assert motor.units == units


@patch("csmotormanager.motor.motor.Motor.get_pv")
def test_motor_string_representation(mock_get_pv):
    name = "x_motor"
    prefix = "MO-MOTORS-01:X"

    motor = Motor(name, prefix)

    string = motor.__str__()

    assert string == "x_motor: MO-MOTORS-01:X"
