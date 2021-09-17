from matplotlib.colors import hsv_to_rgb
from matplotlib.colors import rgb_to_hsv
from matplotlib.colors import to_rgb
from matplotlib.colors import to_hex
import numpy as np

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

    @staticmethod
    def is_rgb_color_values_valid(rgb: list[int]) -> bool:
        if not rgb:
            return False

        for color in rgb:
            if not 0 <= color <= 255:
                return False
        return True


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

    @staticmethod
    def is_hsv_color_values_valid(hsv: list[int]) -> bool:
        if not hsv:
            return False

        if not 0 <= hsv[0] <= 360:
            return False
        if not 0 <= hsv[1] <= 100:
            return False
        if not 0 <= hsv[2] <= 100:
            return False
        return True


class ColorConverter:
    RGB_MAX = 255

    HUE_MAX = 360
    SATURATION_MAX = 100
    VALUE_MAX = 100

    @staticmethod
    # def convert_rgb_to_hsv(rgb_color: RGBColor) -> HSVColor:
    def convert_rgb_to_hsv(r: int, g: int, b: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.rgb_to_hsv.html
        All values assumed to be in range [0, 1]
        """

        rgb_color = RGBColor(r, g, b)
        rgb_color.convert_rgb_max_to_min()
        colors = np.array(rgb_color.to_list())

        hsv_color = HSVColor(*rgb_to_hsv(colors))
        hsv_color.convert_hsv_min_to_max()
        return list(map(lambda c: round(c), hsv_color.to_list()))
        # return hsv_color.to_list()

    # @staticmethod
    # def convert_rgb_to_hsv(r: int, g: int, b: int) -> list[int]:
    #     """
    #     Source:
    #     https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.rgb_to_hsv.html
    #     All values assumed to be in range [0, 1]
    #     """
    #
    #     red, green, blue = r, g, b
    #
    #     if red > 1:
    #         red /= ColorConverter.RGB_MAX
    #     if green > 1:
    #         green /= ColorConverter.RGB_MAX
    #     if blue > 1:
    #         blue /= ColorConverter.RGB_MAX
    #
    #     colors = np.array([red, green, blue])
    #     colors = rgb_to_hsv(colors)
    #
    #     colors[0] *= ColorConverter.HUE_MAX
    #     colors[1] *= ColorConverter.SATURATION_MAX
    #     colors[2] *= ColorConverter.VALUE_MAX
    #
    #     return list(map(lambda c: round(c), colors))

    @staticmethod
    def convert_hsv_to_rgb(h: int, s: int, v: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.hsv_to_rgb.html
        """

        hsv_color = HSVColor(h, s, v)
        hsv_color.convert_hsv_max_to_min()
        colors = np.array(hsv_color.to_list())

        rgb_color = RGBColor(*hsv_to_rgb(colors))
        rgb_color.convert_rgb_min_to_max()
        return list(map(lambda c: round(c), rgb_color.to_list()))
        # return rgb_color.to_list()

    # @staticmethod
    # def convert_hsv_to_rgb(h: int, s: int, v: int) -> list[int]:
    #     """
    #     Source:
    #     https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.hsv_to_rgb.html
    #     """
    #
    #     hue, saturation, value = h, s, v
    #
    #     if hue > 1:
    #         hue /= ColorConverter.HUE_MAX
    #     if saturation > 1:
    #         saturation /= ColorConverter.SATURATION_MAX
    #     if value > 1:
    #         value /= ColorConverter.VALUE_MAX
    #
    #     colors = np.array([hue, saturation, value])
    #     colors = hsv_to_rgb(colors)
    #     colors = list(map(lambda c: c * ColorConverter.RGB_MAX, colors))
    #
    #     return list(map(lambda c: round(c), colors))

    @staticmethod
    def convert_rgb_to_hex(r: int, g: int, b: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_hex.html
        """
        pass

    @staticmethod
    def convert_hex_to_rgb(hex: str) -> list[int]:
        """
        Source:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_rgb.html
        """


def is_rgb_color_values_valid(rgb: list[int]) -> bool:
    if not rgb:
        return False

    for color in rgb:
        if not 0 <= color <= 255:
            return False
    return True


def is_hsv_color_values_valid(hsv: list[int]) -> bool:
    if not hsv:
        return False

    if not 0 <= hsv[0] <= 360:
        return False
    if not 0 <= hsv[1] <= 100:
        return False
    if not 0 <= hsv[2] <= 100:
        return False
    return True
