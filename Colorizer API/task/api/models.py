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

    def operate(self, operation: str) -> None:
        if operation == "saturate":
            self.saturation()
        elif operation == "desaturate":
            self.saturation(desaturate=True)

    def saturation(self, desaturate: bool = False):
        if desaturate:
            self.s_value -= round(self.s_value * (self.amount / 100))
        else:
            self.s_value += round(self.s_value * (self.amount / 100))

        if self.s_value < 0:
            self.s_value = 0
        elif self.s_value > 100:
            self.s_value = 100
