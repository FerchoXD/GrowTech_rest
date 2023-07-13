from rest_framework import generics
from .models import Temperatura
from .api.serializers import TemperaturaSerializer

class TemperaturaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer

class TemperaturaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Temperatura.objects.all()
    serializer_class = TemperaturaSerializer 
