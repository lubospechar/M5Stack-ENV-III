"""Public API for the M5Stack sensor library."""

from .exceptions import SHT30Error, SensorError
from .sht30 import SHT30

__all__ = [
    "SHT30",
    "SHT30Error",
    "SensorError",
]