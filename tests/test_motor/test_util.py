from csmotormanager.motor.util import MotorLimit, find_motor

from ..test_cs.util import MockMotor


class TestFindMotor:
    motor_list = [
        MockMotor("motor_a", "PREFIX:A"),
        MockMotor("motor_b", "PREFIX:B"),
        MockMotor("motor_c", "PREFIX:C"),
    ]

    def test_find_motor_succeeds_for_present_motor(self):
        motor = find_motor("motor_b", self.motor_list)

        assert motor.name == "motor_b"

    def test_find_motor_returns_None_when_not_found(self):
        motor = find_motor("motor_d", self.motor_list)

        assert motor is None

    def test_find_motor_returns_None_for_empty_motor_list(self):
        motor = find_motor("motor_a", [])

        assert motor is None


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
