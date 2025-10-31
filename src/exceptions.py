"""Common exception definitions for M5Stack sensor modules."""

class SensorError(Exception):
    """Base class for all sensor-related errors."""
    pass


class SHT30Error(SensorError):
    """Error related to SHT30 sensor (CRC mismatch, I2C failure, etc.)."""
    pass
