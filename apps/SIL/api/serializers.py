from rest_framework import serializers
from ..models import IntensidadDeLuz


class IntensidadDeLuzSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntensidadDeLuz
        fields = '__all__'