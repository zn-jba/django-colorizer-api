from . import ColorSpace
from .base import Color


class RGBColor(Color):
    def __init__(self, red: int, green: int, blue: int) -> None:
        super().__init__(red, green, blue)

    @property
    def red(self) -> int:
        return self._a

    @red.setter
    def red(self, value: int) -> None:
        self._a = value

    @property
    def green(self) -> int:
        return self._b

    @green.setter
    def green(self, value: int) -> None:
        self._b = value

    @property
    def blue(self) -> int:
        return self._c

    @blue.setter
    def blue(self, value: int) -> None:
        self._c = value

    def to_max_range(self) -> None:
        self.red *= ColorSpace.RGB_MAX
        self.green *= ColorSpace.RGB_MAX
        self.blue *= ColorSpace.RGB_MAX

    def to_min_range(self) -> None:
        self.red /= ColorSpace.RGB_MAX
        self.green /= ColorSpace.RGB_MAX
        self.blue /= ColorSpace.RGB_MAX

    def to_list(self) -> list[int]:
        return [self.red, self.green, self.blue]
