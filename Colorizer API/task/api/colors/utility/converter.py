import numpy as np

import matplotlib.colors as mpl

from ..models.hsv import HSVColor
from ..models.rgb import RGBColor


class ColorConverter:
    @staticmethod
    def convert_rgb_to_hsv(r: int, g: int, b: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.rgb_to_hsv.html
        All values assumed to be in range [0, 1]
        """

        rgb_color = RGBColor(r, g, b)
        rgb_color.convert_rgb_max_to_min()
        colors = np.array(rgb_color.to_list())

        hsv_color = HSVColor(*mpl.rgb_to_hsv(colors))
        hsv_color.convert_hsv_min_to_max()
        return list(map(lambda c: round(c), hsv_color.to_list()))

    @staticmethod
    def convert_hsv_to_rgb(h: int, s: int, v: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.hsv_to_rgb.html
        """

        hsv_color = HSVColor(h, s, v)
        hsv_color.convert_hsv_max_to_min()
        colors = np.array(hsv_color.to_list())

        rgb_color = RGBColor(*mpl.hsv_to_rgb(colors))
        rgb_color.convert_rgb_min_to_max()
        return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def is_rgb_color_values_valid(rgb: list[int]) -> bool:
        if not rgb:
            return False

        for color in rgb:
            if not 0 <= color <= 255:
                return False
        return True

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
