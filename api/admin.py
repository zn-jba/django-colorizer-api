from django.contrib import admin

from .models import HSVColor
from .models import ColorOperation


@admin.register(HSVColor)
class HSVColorAdmin(admin.ModelAdmin):
    list_display = ("representation", "h_value", "s_value", "v_value")


@admin.register(ColorOperation)
class ColorOperationAdmin(admin.ModelAdmin):
    list_display = ("representation", "operation", "amount")

