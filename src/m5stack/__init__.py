"""Public API for the M5Stack sensor library."""

from .exceptions import SensorError, SHT30Error, QMP6988Error
from .sht30 import SHT30
from .qmp6988 import QMP6988

__all__ = [
    "SHT30",
    "SHT30Error",
    "QMP6988",
    "QMP6988Error",
    "SensorError",
]