from rest_framework import generics
from .models import IntensidadDeLuz
from .api.serializers import IntensidadDeLuzSerializer

class IntensidadDeLuzListCreateAPIView(generics.ListCreateAPIView):
    queryset = IntensidadDeLuz.objects.all()
    serializer_class = IntensidadDeLuzSerializer

class IntensidadDeLuzRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntensidadDeLuz.objects.all()
    serializer_class = IntensidadDeLuzSerializer
