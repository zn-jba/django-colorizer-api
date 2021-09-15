from django.contrib import admin

from .models import HSVColor


@admin.register(HSVColor)
class HSVColorAdmin(admin.ModelAdmin):
    list_display = ("representation", "h_value", "s_value", "v_value")
