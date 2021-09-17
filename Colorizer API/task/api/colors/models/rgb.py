from .base import Color


class RGBColor(Color):
    RGB_SMALL_MAX = 1
    RGB_LARGE_MAX = 255

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

    def convert_rgb_min_to_max(self) -> None:
        self.red *= self.RGB_LARGE_MAX
        self.green *= self.RGB_LARGE_MAX
        self.blue *= self.RGB_LARGE_MAX

    def convert_rgb_max_to_min(self) -> None:
        self.red /= self.RGB_SMALL_MAX
        self.green /= self.RGB_SMALL_MAX
        self.blue /= self.RGB_SMALL_MAX

    def to_list(self) -> list[int]:
        return [self.red, self.green, self.blue]
