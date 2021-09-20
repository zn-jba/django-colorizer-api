from django.db import models


class ColorOperation(models.Model):
    representation = models.CharField(max_length=3)
    operation = models.CharField(max_length=20)
    amount = models.IntegerField()

    color_a = models.IntegerField()
    color_b = models.IntegerField()
    color_c = models.IntegerField()

    class Meta:
        ordering = ("operation",)
        verbose_name_plural = "Color Operations"
