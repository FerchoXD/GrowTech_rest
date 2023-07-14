from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.plants.models import Planta,User
from .api.serializers import PlantaSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
class PlantaList(ListAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]

class PlantaCreate(CreateAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]

class PlantaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]


class ValidacionPlants(GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            nombre_planta = data['nombre']
            nombre_usuario = data['nombreU']

            # Verificar si existen los campos en la base de datos
            planta = Planta.objects.get(nombre=nombre_planta)
            usuario = User.objects.get(username=nombre_usuario)

            response_data = {
                'response': 'Los datos existen en la base de datos',
                'id_usuario': usuario.id,
                'id_planta': planta.id,
                'nombre_planta': nombre_planta,
                'nombre_usuario': nombre_usuario,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            # Al menos uno de los campos no existe en la base de datos
            response_data = {
                'response': 'Los datos no existen en la base de datos',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)