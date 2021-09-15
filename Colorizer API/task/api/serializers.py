from rest_framework import serializers

from .models import HSVColor


class HSVColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSVColor
        fields = "__all__"
