import colorsys
import numpy as np
import matplotlib.colors as mpl

from ..models import ColorSpace
from ..models.hsl import HSLColor
from ..models.hsv import HSVColor
from ..models.rgb import RGBColor


class ColorConverter:
    @staticmethod
    def rgb_to_hsv(r: int, g: int, b: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.rgb_to_hsv.html
        All values assumed to be in range [0, 1]
        """
        # colorsys implementation
        rgb_color = RGBColor(r, g, b)
        rgb_color.to_min_range()
        hsv_colors = HSVColor(*colorsys.rgb_to_hsv(*rgb_color.to_list()))
        hsv_colors.to_max_range()
        return hsv_colors.to_list()

        # matplotlib.colors implementation
        # rgb_color = RGBColor(r, g, b)
        # rgb_color.to_min_range()
        # colors = np.array(rgb_color.to_list())
        #
        # hsv_color = HSVColor(*mpl.rgb_to_hsv(colors))
        # hsv_color.to_max_range()
        # return list(map(lambda c: round(c), hsv_color.to_list()))

    @staticmethod
    def hsv_to_rgb(h: int, s: int, v: int) -> list[int]:
        """
        Source:
        https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.hsv_to_rgb.html
        """

        # colorsys implementation
        hsv_colors = HSVColor(h, s, v)
        hsv_colors.to_min_range()
        rgb_colors = RGBColor(*colorsys.hsv_to_rgb(*hsv_colors.to_list()))
        rgb_colors.to_max_range()
        return rgb_colors.to_list()

        # matplotlib.colors implementation
        # hsv_color = HSVColor(h, s, v)
        # hsv_color.to_min_range()
        # colors = np.array(hsv_color.to_list())
        #
        # rgb_color = RGBColor(*mpl.hsv_to_rgb(colors))
        # rgb_color.to_max_range()
        # return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def hex_to_rgb(hex_code: str) -> list[int]:
        """
        Source:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_rgb.html
        """

        # accepted format #rrggbb
        # test if #rgb works : verified, it works
        # NOTE: you get the hex code back in lowercase, the test will require uppercase
        rgb_color = RGBColor(*mpl.to_rgb(hex_code))
        rgb_color.to_max_range()
        return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Converts rgb colors in the 0 ... 255 range to hex code.
        Source:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_hex.html
        """

        # returns the format: ##rrggbb
        rgb_color = RGBColor(r, g, b)
        rgb_color.to_min_range()
        rgb_np = np.array(rgb_color.to_list())
        hex_color = mpl.to_hex(rgb_np)
        return hex_color

    @staticmethod
    def hsv_to_hex(h: int, s: int, v: int) -> str:
        """
        Converts hsv color to hex code consisting of a lowercase
        string in the format #rrggbb.
        """

        hsv_color = HSVColor(h, s, v)
        rgb_color = RGBColor(*ColorConverter.hsv_to_rgb(*hsv_color.to_list()))
        hex_color = ColorConverter.rgb_to_hex(*rgb_color.to_list())
        return hex_color

    @staticmethod
    def hex_to_hsv(hex_code: str) -> list[int]:
        """Converts hex code to hsv color in the larger range."""
        rgb_color = ColorConverter.hex_to_rgb(hex_code)
        hsv_color = HSVColor(*ColorConverter.rgb_to_hsv(*rgb_color))
        return hsv_color.to_list()

    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> list[int]:
        rgb_color = RGBColor(r, g, b)
        rgb_color.to_min_range()
        h, l, s = colorsys.rgb_to_hls(*rgb_color.to_list())
        hsl_color = HSLColor(h, s, l)
        hsl_color.to_max_range()
        return list(map(lambda c: round(c), hsl_color.to_list()))

    @staticmethod
    def hsl_to_rgb(h: int, s: int, l: int) -> list[int]:
        hsl_color = HSLColor(h, s, l)
        hsl_color.to_min_range()
        rgb_color = RGBColor(*colorsys.hls_to_rgb(
            h=hsl_color.hue,
            l=hsl_color.light,
            s=hsl_color.saturation))
        rgb_color.to_max_range()
        return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def is_rgb_color_valid(rgb: list[int]) -> bool:
        if not rgb:
            return False

        for color in rgb:
            if not 0 <= color <= ColorSpace.RGB_MAX:
                return False
        return True

    @staticmethod
    def hsl_to_hex(h: int, s: int, l: int) -> str:
        hsl_colors = HSLColor(h, s, l)
        rgb_colors = ColorConverter.hsl_to_rgb(*hsl_colors.to_list())
        rgb_colors = RGBColor(*rgb_colors)
        hex_code = ColorConverter.rgb_to_hex(*rgb_colors.to_list())
        return hex_code

    @staticmethod
    def hex_to_hsl(hex_code: str) -> list[int]:
        rgb_colors = ColorConverter.hex_to_rgb(hex_code)
        hsl_colors = ColorConverter.rgb_to_hsl(*rgb_colors)
        return hsl_colors

    @staticmethod
    def is_hsv_color_valid(hsv: list[int]) -> bool:
        if not hsv:
            return False

        if not 0 <= hsv[0] <= ColorSpace.HUE_MAX:
            return False
        if not 0 <= hsv[1] <= ColorSpace.SATURATION_MAX:
            return False
        if not 0 <= hsv[2] <= ColorSpace.VALUE_MAX:
            return False
        return True

    @staticmethod
    def is_hsl_color_valid(hsl: list[int]) -> bool:
        if not hsl:
            return False

        if not 0 <= hsl[0] <= ColorSpace.HUE_MAX:
            return False
        if not 0 <= hsl[1] <= ColorSpace.SATURATION_MAX:
            return False
        if not 0 <= hsl[2] <= ColorSpace.LIGHT_MAX:
            return False
        return True

    @staticmethod
    def is_hex_code_valid(hex_code: str) -> bool:
        pass
