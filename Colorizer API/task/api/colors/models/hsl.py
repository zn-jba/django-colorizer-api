from . import ColorSpace
from .base import Color


class HSLColor(Color):
    def __init__(self, h: int, s: int, l: int) -> None:
        super().__init__(h, s, l)

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
    def light(self) -> int:
        return self._c

    @light.setter
    def light(self, value: int) -> None:
        self._c = value

    def to_max_range(self) -> None:
        self.hue *= ColorSpace.HUE_MAX
        self.saturation *= ColorSpace.SATURATION_MAX
        self.light *= ColorSpace.LIGHT_MAX

    def to_min_range(self) -> None:
        self.hue /= ColorSpace.HUE_MAX
        self.saturation /= ColorSpace.SATURATION_MAX
        self.light /= ColorSpace.LIGHT_MAX

    def to_list(self) -> list[int]:
        return [self.hue, self.saturation, self.light]
