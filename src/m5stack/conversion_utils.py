"""Utility functions for converting raw sensor values to physical units."""

from dataclasses import dataclass
from typing import Optional


def raw_to_celsius(raw: int) -> float:
    """Convert 16-bit raw temperature to degrees Celsius (SHT30 formula).

    Formula: T(°C) = -45 + 175 * (raw / 65535.0)
    """
    return -45.0 + 175.0 * (raw / 65535.0)


def raw_to_humidity(raw: int) -> float:
    """Convert 16-bit raw humidity to relative humidity in %.

    Formula: RH(%) = 100 * (raw / 65535.0)
    """
    rh = 100.0 * (raw / 65535.0)
    # Clamp between 0 and 100
    return max(0.0, min(100.0, rh))


def raw_to_pascal(
    raw: int,
    coef_a: float = 0.01,
    coef_b: float = 0.0,
) -> float:
    return coef_a * raw + coef_b

