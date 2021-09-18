from django.db import models


class HSVColor(models.Model):
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
