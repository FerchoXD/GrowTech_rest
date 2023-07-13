from rest_framework import serializers
from ..models import HumedadDeSuelo


class HumedadDeSueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumedadDeSuelo
        fields = '__all__'