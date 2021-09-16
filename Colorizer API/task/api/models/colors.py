from django.db import models


class HSVColor(models.Model):
    HSV_OPERATIONS = ("saturate", "desaturate")

    representation = models.CharField(max_length=3)
    h_value = models.PositiveIntegerField()
    s_value = models.PositiveIntegerField()
    v_value = models.PositiveIntegerField()
    operation = models.CharField(max_length=20)
    amount = models.IntegerField()

    class Meta:
        verbose_name_plural = "HSV colors"

    def __init__(self, data: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.representation = data.get("representation", None)
        self.h_value = data.get("color", None)[0]
        self.s_value = data.get("color", None)[1]
        self.v_value = data.get("color", None)[2]
        self.operation = data.get("operation", None)
        self.amount = data.get("amount", None)

    @property
    def colors(self) -> tuple[int, int, int]:
        return self.h_value, self.s_value, self.v_value

    def operate(self, operation: str, commit: bool = False) -> dict:
        modified_data = {
            "representation": self.representation,
            "color": [*self.colors],
            "operation": self.operation
        }

        if operation == "saturate":
            self.saturation(commit)
        elif operation == "desaturate":
            self.saturation(commit, desaturate=True)

        modified_data["modified_color"] = [*self.colors]
        return modified_data

    def saturation(self, commit: bool, desaturate: bool = False):
        if desaturate:
            value = self.s_value - round(self.s_value * (self.amount / 100))
        else:
            value = self.s_value + round(self.s_value * (self.amount / 100))

        if value < 0:
            value = 0
        elif value > 100:
            value = 100

        if commit:
            self.s_value = value
