from .base import Color


class HSVColor(Color):
    HUE_MAX = 360
    SATURATION_MAX = 100
    VALUE_MAX = 100

    def __init__(self, hue: int, saturation: int, value: int) -> None:
        super().__init__(hue, saturation, value)

    @property
    def hue(self) -> int:
        return self._a

    @hue.setter
    def hue(self, value: int) -> None:
        self._a = value

    @property
    def saturation(self) -> int:
        return self._b

    @saturation.setter
    def saturation(self, value: int) -> None:
        self._b = value

    @property
    def value(self) -> int:
        return self._c

    @value.setter
    def value(self, value: int) -> None:
        self._c = value

    def convert_hsv_min_to_max(self) -> None:
        self.hue *= self.HUE_MAX
        self.saturation *= self.SATURATION_MAX
        self.value *= self.VALUE_MAX

    def convert_hsv_max_to_min(self) -> None:
        self.hue /= self.HUE_MAX
        self.saturation /= self.SATURATION_MAX
        self.value /= self.VALUE_MAX

    def to_list(self) -> list[int]:
        return [self.hue, self.saturation, self.value]
