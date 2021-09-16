from rest_framework import serializers

from ..models.operations import ColorOperation


class ColorOperationSerializer(serializers.ModelSerializer):
    # color = serializers.SerializerMethodField()

    class Meta:
        model = ColorOperation
        fields = ("representation", "operation", "color_a", "color_b", "color_c", "amount")
        # fields = "__all__"
        # exclude = ("id", "color_a", "color_b", "color_c")

    # def get_color(self, object: ColorOperation) -> list[int]:
    #     return [
    #         object.color_a,
    #         object.color_b,
    #         object.color_c
    #     ]

    def to_internal_value(self, data):
        data["color_a"], data["color_b"], data["color_c"] = data["color"]
        data.pop("color")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["color"] = [instance.color_a, instance.color_b, instance.color_c]
        data.pop("color_a")
        data.pop("color_b")
        data.pop("color_c")
        return data
