from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.plants.models import Planta, User
from .api.serializers import PlantaSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from apps.ST.models import Temperatura
from apps.SHS.models import HumedadDeSuelo
from apps.SHA.models import HumedadDeAmbiente
from apps.SIL.models import IntensidadDeLuz
from .api.serializers import DataSerializer
from django.db.models import Avg


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


class PlantaListByUser(ListAPIView):
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Planta.objects.filter(usuario_id=user_id)


class DatosPromedios(GenericAPIView):
    serializer_class = DataSerializer

    def post(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario_id')

        try:
            usuario = User.objects.get(id=usuario_id)
        except ObjectDoesNotExist:
            response_data = {
                'error': 'El usuario con el ID proporcionado no existe.',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        intensidad_promedio = IntensidadDeLuz.objects.filter(planta__usuario_id=usuario_id).values(
            'fecha_hora').annotate(valor_avg=Avg('valor')).values('fecha_hora', 'valor_avg')

        temperatura_promedio = Temperatura.objects.filter(planta__usuario_id=usuario_id).values(
            'fecha_hora').annotate(valor_avg=Avg('valor')).values('fecha_hora', 'valor_avg')

        humedad_suelo_promedio = HumedadDeSuelo.objects.filter(planta__usuario_id=usuario_id).values(
            'fecha_hora').annotate(valor_avg=Avg('valor')).values('fecha_hora', 'valor_avg')

        humedad_ambiente_promedio = HumedadDeAmbiente.objects.filter(planta__usuario_id=usuario_id).values(
            'fecha_hora').annotate(valor_avg=Avg('valor')).values('fecha_hora', 'valor_avg')

        data = {
    'usuario_id': usuario_id,
    'fecha_hora': intensidad_promedio[0]['fecha_hora'].strftime('%Y-%m-%d %H:%M:%S') if intensidad_promedio else None,
    'intensidad_promedio': intensidad_promedio[0]['valor_avg'] if intensidad_promedio else None,
    'temperatura_promedio': temperatura_promedio[0]['valor_avg'] if temperatura_promedio else None,
    'humedad_suelo_promedio': humedad_suelo_promedio[0]['valor_avg'] if humedad_suelo_promedio else None,
    'humedad_ambiente_promedio': humedad_ambiente_promedio[0]['valor_avg'] if humedad_ambiente_promedio else None
}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_200_OK)

