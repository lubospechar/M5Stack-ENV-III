"""SHT30 frame parsing and CRC validation."""

from m5stack.crc_utils import crc8_sht
from m5stack.exceptions import SHT30Error


def parse_measurement_frame(frame: bytes) -> tuple[int, int]:
    """Parse a 6-byte SHT30 measurement frame and validate its CRC checksums.

    The frame layout is:
        [0] temperature_high_byte
        [1] temperature_low_byte
        [2] temperature_crc
        [3] humidity_high_byte
        [4] humidity_low_byte
        [5] humidity_crc
    """
    if len(frame) != 6:
        raise SHT30Error(f"Invalid frame length: {len(frame)} (expected 6 bytes)")

    # Split frame into temperature and humidity parts
    temperature_raw_bytes = frame[0:2]
    temperature_crc_byte = frame[2]
    humidity_raw_bytes = frame[3:5]
    humidity_crc_byte = frame[5]

    # Validate temperature CRC
    calculated_temperature_crc = crc8_sht(temperature_raw_bytes)
    if calculated_temperature_crc != temperature_crc_byte:
        raise SHT30Error(
            f"CRC mismatch (temperature): received 0x{temperature_crc_byte:02X}, "
            f"expected 0x{calculated_temperature_crc:02X}"
        )

    # Validate humidity CRC
    calculated_humidity_crc = crc8_sht(humidity_raw_bytes)
    if calculated_humidity_crc != humidity_crc_byte:
        raise SHT30Error(
            f"CRC mismatch (humidity): received 0x{humidity_crc_byte:02X}, "
            f"expected 0x{calculated_humidity_crc:02X}"
        )

    # Combine two bytes into 16-bit integers (big-endian)
    temperature_raw_value = (temperature_raw_bytes[0] << 8) | temperature_raw_bytes[1]
    humidity_raw_value = (humidity_raw_bytes[0] << 8) | humidity_raw_bytes[1]

    return temperature_raw_value, humidity_raw_value
