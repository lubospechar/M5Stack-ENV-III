"""Utility functions for converting raw sensor values to physical units."""


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


def raw_to_pascal(raw: int, coef_a: float = 1.0, coef_b: float = 0.0) -> float:
    """Convert 24-bit raw pressure to Pascals (QMP6988 simplified formula).

    The full formula uses calibration coefficients read from the sensor’s NVM.
    This simplified placeholder assumes a linear mapping:
        P(Pa) = coef_a * raw + coef_b

    Parameters
    ----------
    raw : int
        24-bit raw pressure value from the ADC.
    coef_a, coef_b : float
        Calibration coefficients (to be set after reading trim data).

    Returns
    -------
    float
        Approximate pressure in Pascals.
    """
    return coef_a * raw + coef_b
