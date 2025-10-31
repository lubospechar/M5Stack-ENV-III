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


# conversion_utils.py
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


# --- QMP6988: plná kompenzace -------------------------------------------------

@dataclass(slots=True)
class Qmp6988Coefficients:
    """Kalibrační koeficienty QMP6988 (přepočtené z OTP podle datasheetu).

    Očekává se sada koeficientů:
        a0, a1, a2, b00, bt1, bp1, b11, bt2, bp2, b12, b21, bp3

    Jednotky a vzorce viz datasheet QMP6988 (Tr a Pr níže).
    """
    a0: float
    a1: float
    a2: float
    b00: float
    bt1: float
    bp1: float
    b11: float
    bt2: float
    bp2: float
    b12: float
    b21: float
    bp3: float


def raw_to_pascal(
    raw: int,
    coef_a: float = 1.0,
    coef_b: float = 0.0,
    *,
    qmp: Optional[Qmp6988Coefficients] = None,
    dt: Optional[int] = None,
) -> float:
    """Convert raw pressure to Pascals.

    Dvojí režim:
      1) QMP6988 plná kompenzace — když jsou zadány `qmp` (koeficienty) a `dt` (raw teplota).
         Pak počítá:
             Tr = a0 + a1*Dt + a2*Dt^2    (Tr v jednotkách 256*°C)
             Pr = b00 + bt1*Tr + bp1*Dp + b11*Tr*Dp + bt2*Tr^2 + bp2*Dp^2
                  + b12*Dp*Tr^2 + b21*Dp^2*Tr + bp3*Dp^3
         kde Dp = `raw` (signed 24-bit po odečtu 2^23), Dt je totéž pro teplotu.
         Viz QMP6988 datasheet, sekce 4.3–4.4. :contentReference[oaicite:0]{index=0}

      2) Lineární placeholder — pokud `qmp` nebo `dt` nejsou zadány:
             P = coef_a * raw + coef_b
         (zpětně kompatibilní chování pro jednoduché škálování)

    Parametry
    ---------
    raw : int
        Dp – surový tlak (signed 24-bit po odečtu 2^23).
    coef_a, coef_b : float
        Koeficienty pro lineární režim (fallback).
    qmp : Qmp6988Coefficients | None
        Přepočtené kalibrační koeficienty senzoru.
    dt : int | None
        Dt – surová teplota (signed 24-bit po odečtu 2^23).

    Návrat
    ------
    float
        Tlak v Pascalech.
    """
    if qmp is not None and dt is not None:
        Tr = qmp.a0 + qmp.a1 * dt + qmp.a2 * (dt * dt)
        Dp = float(raw)

        Pr = (
            qmp.b00
            + qmp.bt1 * Tr
            + qmp.bp1 * Dp
            + qmp.b11 * Tr * Dp
            + qmp.bt2 * (Tr * Tr)
            + qmp.bp2 * (Dp * Dp)
            + qmp.b12 * Dp * (Tr * Tr)
            + qmp.b21 * (Dp * Dp) * Tr
            + qmp.bp3 * (Dp * Dp * Dp)
        )
        return float(Pr)

    # Fallback: jednoduché škálování (zachovává stávající chování)
    return coef_a * raw + coef_b

