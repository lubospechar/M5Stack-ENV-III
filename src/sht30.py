from typing import Protocol, runtime_checkable, Tuple

@runtime_checkable
class ISHT30(Protocol):
    bus_num: int
    address: int

    def read(self) -> tuple[float, float]: ...
    def read_temperature(self) -> float: ...
    def read_humidity(self) -> float: ...