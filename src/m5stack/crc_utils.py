"""Utility functions for computing CRC checksums used by sensor drivers."""

def crc8_sht(data: bytes) -> int:
    """Compute CRC-8 checksum for SHT30/SHT31 sensors (poly=0x31, init=0xFF)."""
    polynomial = 0x31   # x^8 + x^5 + x^4 + 1
    init_value = 0xFF
    width = 8

    crc = init_value
    for b in data:
        crc = _crc8_apply_byte(crc, b, polynomial, width)
    return crc


def _crc8_apply_byte(crc: int, byte: int, polynomial: int, width: int) -> int:
    """Integrate one data byte into the CRC register."""
    crc ^= byte
    for _ in range(width):
        crc = _crc8_shift_once(crc, polynomial, width)
    return crc & 0xFF


def _crc8_shift_once(crc: int, polynomial: int, width: int) -> int:
    """Perform one CRC register shift and conditional polynomial XOR."""
    msb_mask = 1 << (width - 1)
    msb_set = bool(crc & msb_mask)
    crc = (crc << 1) & 0xFF
    if msb_set:
        crc ^= polynomial
    return crc
