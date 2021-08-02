from csmotormanager.motor import Motor
from csmotormanager.util import pv


class MockMotor(Motor):
    """Motor class which doesn't use channel access"""

    def get_pv(self, field: str) -> pv:
        if field == "EGU":
            return "mm"
        elif field == "RBV":
            return 5.5
        elif field == "HLM":
            return 10.0
        elif field == "LLM":
            return -10.0
        else:
            return 0.0
