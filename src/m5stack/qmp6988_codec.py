"""QMP6988 frame parsing (pressure-only, no CRC)."""

from m5stack.exceptions import QMP6988Error


def parse_pressure_frame(frame: bytes) -> int:
    """Parse a 3-byte QMP6988 pressure frame (no CRC present).

    Layout:
        [0] pressure_msb
        [1] pressure_lsb
        [2] pressure_xlsb

    Returns
    -------
    int
        24-bit raw pressure value.
    """
    if len(frame) != 3:
        raise QMP6988Error(f"Invalid frame length: {len(frame)} (expected 3 bytes)")

    return (frame[0] << 16) | (frame[1] << 8) | frame[2]
