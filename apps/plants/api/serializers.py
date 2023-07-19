from rest_framework import serializers
from apps.plants.models import Planta

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

class DataSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    fecha_hora = serializers.DateTimeField()
    intensidad_promedio = serializers.FloatField()
    temperatura_promedio = serializers.FloatField()
    humedad_suelo_promedio = serializers.FloatField()
    humedad_ambiente_promedio = serializers.FloatField()



class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ['id', 'nombre']