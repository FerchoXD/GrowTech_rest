from rest_framework import generics
from .models import HumedadDeAmbiente
from .api.serializers import HumedadDeAmbienteSerializer

class HumedadDeAmbienteListCreateAPIView(generics.ListCreateAPIView):
    queryset = HumedadDeAmbiente.objects.all()
    serializer_class = HumedadDeAmbienteSerializer

class HumedadDeAmbienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HumedadDeAmbiente.objects.all()
    serializer_class = HumedadDeAmbienteSerializer
