from matplotlib.colors import hsv_to_rgb
from matplotlib.colors import rgb_to_hsv
import numpy as np


class ColorConverter:
    RGB_MAX = 255

    HUE_MAX = 360
    SATURATION_MAX = 100
    VALUE_MAX = 100

    @staticmethod
    def convert_rgb_to_hsv(r: int, g: int, b: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.rgb_to_hsv.html
        All values assumed to be in range [0, 1]
        """

        red, green, blue = r, g, b

        if red > 1:
            red /= ColorConverter.RGB_MAX
        if green > 1:
            green /= ColorConverter.RGB_MAX
        if blue > 1:
            blue /= ColorConverter.RGB_MAX

        colors = np.array([red, green, blue])
        colors = rgb_to_hsv(colors)

        colors[0] *= ColorConverter.HUE_MAX
        colors[1] *= ColorConverter.SATURATION_MAX
        colors[2] *= ColorConverter.VALUE_MAX

        return list(map(lambda c: round(c), colors))

    @staticmethod
    def convert_hsv_to_rgb(h: int, s: int, v: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.hsv_to_rgb.html
        """

        hue, saturation, value = h, s, v

        if hue > 1:
            hue /= ColorConverter.HUE_MAX
        if saturation > 1:
            saturation /= ColorConverter.SATURATION_MAX
        if value > 1:
            value /= ColorConverter.VALUE_MAX

        colors = np.array([hue, saturation, value])
        colors = hsv_to_rgb(colors)
        colors = list(map(lambda c: c * ColorConverter.RGB_MAX, colors))

        return list(map(lambda c: round(c), colors))


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
