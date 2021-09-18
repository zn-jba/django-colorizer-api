from ..models.hsv import HSVColor


class ColorModifier:
    HSV_OPERATIONS = ("saturate", "desaturate")

    @staticmethod
    def modify(representation: str,
               operation: str,
               amount: int,
               color: list[int]) -> list[int]:
        if operation == "saturate":
            return ColorModifier.saturation(amount, color)
        elif operation == "desaturate":
            return ColorModifier.saturation(amount, color, desaturate=True)

    @staticmethod
    def saturation(amount: int, color: list[int], desaturate: bool = False) -> list[int]:
        hsv_color = HSVColor(*color)
        if desaturate:
            hsv_color.saturation -= round(hsv_color.saturation * (amount / 100))
        else:
            hsv_color.saturation += round(hsv_color.saturation * (amount / 100))

        if hsv_color.saturation < 0:
            hsv_color.saturation = 0
        elif hsv_color.saturation > 100:
            hsv_color.saturation = 100
        return hsv_color.to_list()
