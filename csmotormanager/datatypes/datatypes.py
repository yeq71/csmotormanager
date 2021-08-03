from dataclasses import dataclass
from typing import Union

from cothread.dbr import ca_array, ca_float, ca_int, ca_str

# PV type for type hints
pv = Union[ca_array, ca_float, ca_int, ca_str]


@dataclass
class Parameter:
    """Parameter data class"""

    name: str
    value: float

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"
