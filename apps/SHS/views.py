from rest_framework import generics
from .models import HumedadDeSuelo
from .api.serializers import HumedadDeSueloSerializer

class HumedadDeSueloListCreateAPIView(generics.ListCreateAPIView):
    queryset = HumedadDeSuelo.objects.all()
    serializer_class = HumedadDeSueloSerializer

class HumedadDeSueloRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HumedadDeSuelo.objects.all()
    serializer_class = HumedadDeSueloSerializer
