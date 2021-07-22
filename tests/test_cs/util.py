from csmotormanager.motor import Motor


class MockMotor(Motor):
    """Motor class which doesn't use channel access"""

    def get_pv(self, field: str) -> None:
        pass
