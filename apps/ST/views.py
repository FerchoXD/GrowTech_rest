from rest_framework import generics
from .models import Temperatura
from .api.serializers import TemperaturaSerializer
from .models import Temperatura
from .api.serializers import TemperaturaSerializer
class TemperaturaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer

class TemperaturaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer 

class UltimoDatoTemperaturaAPIView(generics.ListAPIView):
    queryset = Temperatura.objects.order_by('-fecha_hora')[:1]
    serializer_class = TemperaturaSerializer