from typing import Tuple, Union

import cothread.catools
from cothread.dbr import ca_array, ca_float, ca_int, ca_str

pv = Union[ca_array, ca_float, ca_int, ca_str]


class Motor:
    def __init__(self, name: str, prefix: str):
        self.name: str = name
        self.prefix: str = prefix
        self.units: str = self.get_pv("EGU")

    def __str__(self):
        return f"{self.name}: {self.prefix}"

    def get_position(self) -> float:
        return self.get_pv("RBV")

    def get_limits(self) -> Tuple[ca_float, ca_float]:
        low_limit = self.get_pv("LLM")
        high_limit = self.get_pv("HLM")
        return (low_limit, high_limit)

    def get_pv(self, field: str) -> pv:
        return cothread.catools.caget(f"{self.prefix}.{field}")

    def get_report_string(self) -> str:
        position = self.get_position()
        low_limit, high_limit = self.get_limits()
        return f"{self.name}: {position:f}{self.units} [{low_limit}, {high_limit}]"
