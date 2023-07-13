from rest_framework import serializers
from ..models import HumedadDeAmbiente


class HumedadDeAmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumedadDeAmbiente
        fields = '__all__'