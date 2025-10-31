from typing import Protocol, runtime_checkable
from dataclasses import dataclass
from m5stack.exceptions import SHT30Error

@runtime_checkable
class ISHT30(Protocol):
    """Protocol (interface) for reading data from an SHT30 sensor."""

    bus_num: int
    address: int

    def read(self) -> tuple[float, float]:
        """Return a tuple (temperature °C, relative humidity %RH)."""
        ...

    def read_temperature(self) -> float:
        """Return the temperature in Celsius."""
        ...

    def read_humidity(self) -> float:
        """Return the relative humidity in percent."""
        ...

@dataclass(slots=True)
class SHT30:
    bus_num: int = 1
    address: int = 0x44

    def read(self):
        return [0.5, 0.5]

    def read_temperature(self):
        return 0.5

    def read_humidity(self):
        return 0.5
