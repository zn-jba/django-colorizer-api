from abc import ABC
from abc import abstractmethod


class Color(ABC):
    def __init__(self, a, b, c) -> None:
        self._a = a
        self._b = b
        self._c = c

    @abstractmethod
    def to_list(self) -> list[int]:
        ...

    @abstractmethod
    def to_min_range(self) -> None:
        ...

    @abstractmethod
    def to_max_range(self) -> None:
        ...
