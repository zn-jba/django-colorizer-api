from .base import Color
from .base import ColorSpace


class HSVColor(Color):
    def __init__(self, hue: int, saturation: int, value: int) -> None:
        super().__init__(hue, saturation, value)

    @property
    def hue(self) -> int:
        return self._a

    @hue.setter
    def hue(self, new_value: int) -> None:
        self._a = new_value

    @property
    def saturation(self) -> int:
        return self._b

    @saturation.setter
    def saturation(self, new_value: int) -> None:
        self._b = new_value

    @property
    def value(self) -> int:
        return self._c

    @value.setter
    def value(self, new_value: int) -> None:
        self._c = new_value

    def to_max_range(self) -> None:
        self.hue *= ColorSpace.HUE_MAX
        self.saturation *= ColorSpace.SATURATION_MAX
        self.value *= ColorSpace.VALUE_MAX

    def to_min_range(self) -> None:
        self.hue /= ColorSpace.HUE_MAX
        self.saturation /= ColorSpace.SATURATION_MAX
        self.value /= ColorSpace.VALUE_MAX

    def to_list(self) -> list[int]:
        return [self.hue, self.saturation, self.value]
