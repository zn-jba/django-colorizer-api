"""
Source:
https://docs.python.org/3/library/colorsys.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_rgb.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.to_hex.html

# ColorHarmonifier.complementary() credit goes to Hubert Sieczka
https://numpy.org/doc/stable/reference/generated/numpy.interp.html
"""

import colorsys
from numpy import interp
import re

import matplotlib.colors as mpl

from ..models.base import ColorSpace
from ..models.hsl import HSLColor
from ..models.hsv import HSVColor
from ..models.rgb import RGBColor


class ColorConverter:
    COLOR_SPACE_MODELS = ("hex", "hsl", "hsv", "rgb")

    @staticmethod
    def convert(from_: str, to: str, color: list[int] or str) -> list[int]:
        return CONVERT[from_][to](color)

    @staticmethod
    def round(color: list[int]) -> list[int]:
        return list(map(lambda c: round(c), color))

    @staticmethod
    def rgb_to_hsv(rgb: list[int]) -> list[int]:
        """"""

        rgb_color = RGBColor(*rgb)
        rgb_color.to_min_range()
        hsv_colors = HSVColor(*colorsys.rgb_to_hsv(*rgb_color.to_list()))
        hsv_colors.to_max_range()
        return ColorConverter.round(hsv_colors.to_list())

    @staticmethod
    def hsv_to_rgb(hsv: list[int]) -> list[int]:
        """"""

        hsv_colors = HSVColor(*hsv)
        hsv_colors.to_min_range()
        rgb_colors = RGBColor(*colorsys.hsv_to_rgb(*hsv_colors.to_list()))
        rgb_colors.to_max_range()
        return list(map(lambda c: round(c), rgb_colors.to_list()))

    @staticmethod
    def hex_to_rgb(hex_code: str) -> list[int]:
        rgb_color = RGBColor(*mpl.to_rgb(hex_code))
        rgb_color.to_max_range()
        return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def rgb_to_hex(rgb: list[int]) -> str:
        """
        Converts rgb colors in the 0 ... 255 range to hex code
        and returns it as a string in the format #rrggbb.
        """

        rgb_color = RGBColor(*rgb)
        rgb_color.to_min_range()
        hex_color = mpl.to_hex(rgb_color.to_list())
        return hex_color.upper()

    @staticmethod
    def hsv_to_hex(hsv: list[int]) -> str:
        """
        Converts hsv color to hex code consisting of a lowercase
        string in the format #rrggbb.
        """

        hsv_color = HSVColor(*hsv)
        rgb_color = RGBColor(*ColorConverter.hsv_to_rgb(hsv_color.to_list()))
        hex_color = ColorConverter.rgb_to_hex(rgb_color.to_list())
        return hex_color.upper()

    @staticmethod
    def hex_to_hsv(hex_code: str) -> list[int]:
        """Converts hex code to hsv color in the larger range."""
        rgb_color = ColorConverter.hex_to_rgb(hex_code)
        hsv_color = HSVColor(*ColorConverter.rgb_to_hsv(rgb_color))
        return list(map(lambda c: round(c), hsv_color.to_list()))

    @staticmethod
    def rgb_to_hsl(rgb: list[int]) -> list[int]:
        rgb_color = RGBColor(*rgb)
        rgb_color.to_min_range()
        h, l, s = colorsys.rgb_to_hls(*rgb_color.to_list())
        hsl_color = HSLColor(h, s, l)
        hsl_color.to_max_range()
        return list(map(lambda c: round(c), hsl_color.to_list()))

    @staticmethod
    def hsl_to_rgb(hsl: list[int]) -> list[int]:
        hsl_color = HSLColor(*hsl)
        hsl_color.to_min_range()
        rgb_color = RGBColor(*colorsys.hls_to_rgb(
            h=hsl_color.hue,
            l=hsl_color.light,
            s=hsl_color.saturation))
        rgb_color.to_max_range()
        return list(map(lambda c: round(c), rgb_color.to_list()))

    @staticmethod
    def hsl_to_hsv(hsl: list[int]) -> list[int]:
        hsl_color = HSLColor(*hsl)
        hsl_color.to_min_range()
        rgb_color = RGBColor(*colorsys.hls_to_rgb(
            h=hsl_color.hue,
            l=hsl_color.light,
            s=hsl_color.saturation))
        hsv_color = HSVColor(*colorsys.rgb_to_hsv(*rgb_color.to_list()))
        hsv_color.to_max_range()
        return list(map(lambda c: round(c), hsv_color.to_list()))

    @staticmethod
    def hsv_to_hsl(hsv: list[int]) -> list[int]:
        hsv_color = HSVColor(*hsv)
        hsv_color.to_min_range()
        rgb_color = RGBColor(*colorsys.hsv_to_rgb(*hsv_color.to_list()))
        hsl_color = HSLColor(*colorsys.rgb_to_hls(*rgb_color.to_list()))
        hsl_color.saturation, hsl_color.light = hsl_color.light, hsl_color.saturation
        hsl_color.to_max_range()
        return list(map(lambda c: round(c), hsl_color.to_list()))

    @staticmethod
    def hsl_to_hex(hsl: list[int]) -> str:
        hsl_colors = HSLColor(*hsl)
        rgb_colors = ColorConverter.hsl_to_rgb(hsl_colors.to_list())
        rgb_colors = RGBColor(*rgb_colors)
        hex_code = ColorConverter.rgb_to_hex(rgb_colors.to_list())
        return hex_code.upper()

    @staticmethod
    def hex_to_hsl(hex_code: str) -> list[int]:
        rgb_colors = ColorConverter.hex_to_rgb(hex_code)
        hsl_colors = ColorConverter.rgb_to_hsl(rgb_colors)
        return hsl_colors


class ColorHarmonifier:
    @staticmethod
    def monochromatic(hsv: list[int]) -> dict:
        base = hsv[2]

        if base < 20:
            monochromatic = [base, base + 20, base + 40]
        elif 20 <= base <= 80:
            monochromatic = [base - 20, base, base + 20]
        else:
            monochromatic = [base - 40, base - 20, base]

        result = dict()
        for index, value in enumerate(monochromatic):
            result[f"color_{index + 1}"] = [hsv[0], hsv[1], value]
        return result

    @staticmethod
    def complementary(hsv: list[int]) -> list[int]:
        original_hue = hsv[0]

        temp_hue = interp(original_hue, list(ColorWheel.ADOBE.keys()),
                          list(ColorWheel.ADOBE.values()))
        temp_hue += 180
        if temp_hue > 360:
            temp_hue -= 360

        complementary_hue = round(interp(temp_hue, list(ColorWheel.ADOBE.values()),
                                         list(ColorWheel.ADOBE.keys())))
        return [complementary_hue, hsv[1], hsv[2]]


class ColorValidator:
    @staticmethod
    def is_color_valid(representation: str, color: list[int] or str) -> bool:
        if not color:
            return False
        return COLOR_VALIDATORS[representation](color)

    @staticmethod
    def is_hex_code_valid(hex_code: str) -> bool:
        return bool(re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_code.lower()))

    @staticmethod
    def is_hsl_color_valid(hsl: list[int]) -> bool:
        max_ranges = [ColorSpace.HUE_MAX, ColorSpace.SATURATION_MAX, ColorSpace.LIGHT_MAX]
        return all([0 <= value <= max_range for value, max_range in zip(hsl, max_ranges)])

    @staticmethod
    def is_hsv_color_valid(hsv: list[int]) -> bool:
        max_ranges = [ColorSpace.HUE_MAX, ColorSpace.SATURATION_MAX, ColorSpace.VALUE_MAX]
        return all([0 <= value <= max_range for value, max_range in zip(hsv, max_ranges)])

    @staticmethod
    def is_rgb_color_valid(rgb: list[int]) -> bool:
        return all([0 <= color <= ColorSpace.RGB_MAX for color in rgb])


class ColorWheel:
    ADOBE = {
        0: 0,  # red
        35: 60,  # orange
        60: 122,  # yellow
        120: 165,  # green
        180: 218,  # cyan
        240: 275,  # blue
        300: 330,  # magenta
        360: 360  # red
    }


CONVERT = {
    "hex": {
        "hsl": ColorConverter.hex_to_hsl,
        "hsv": ColorConverter.hex_to_hsv,
        "rgb": ColorConverter.hex_to_rgb
    },
    "hsl": {
        "hex": ColorConverter.hsl_to_hex,
        "hsv": ColorConverter.hsl_to_hsv,
        "rgb": ColorConverter.hsl_to_rgb
    },
    "hsv": {
        "hex": ColorConverter.hsv_to_hex,
        "hsl": ColorConverter.hsv_to_hsl,
        "rgb": ColorConverter.hsv_to_rgb
    },
    "rgb": {
        "hex": ColorConverter.rgb_to_hex,
        "hsl": ColorConverter.rgb_to_hsl,
        "hsv": ColorConverter.rgb_to_hsv
    }
}

COLOR_VALIDATORS = {
    "hex": ColorValidator.is_hex_code_valid,
    "hsl": ColorValidator.is_hsl_color_valid,
    "hsv": ColorValidator.is_hsv_color_valid,
    "rgb": ColorValidator.is_rgb_color_valid
}
