from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.plants.models import Planta, User
from .api.serializers import PlantaSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from apps.plants.api.serializers import ConsultaSerializer
from apps.ST.models import Temperatura
from apps.SHS.models import HumedadDeSuelo
from apps.SHA.models import HumedadDeAmbiente
from apps.SIL.models import IntensidadDeLuz
from .api.serializers import DataSerializer
from datetime import datetime, time
from django.db.models import Avg
from django.db.models.functions import TruncDate
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


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
        planta_id = request.data.get('planta_id')

        try:
            usuario = User.objects.get(id=usuario_id)
        except ObjectDoesNotExist:
            response_data = {
                'error': 'El usuario con el ID proporcionado no existe.',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            planta = Planta.objects.get(id=planta_id, usuario=usuario)
        except ObjectDoesNotExist:
            response_data = {
                'error': 'La planta con el ID proporcionado no existe para este usuario.',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        intensidad_promedio = IntensidadDeLuz.objects.filter(planta=planta).annotate(
            dia=TruncDate('fecha_hora')
        ).values('dia').annotate(valor_avg=Avg('valor')).values('dia', 'valor_avg')

        temperatura_promedio = Temperatura.objects.filter(planta=planta).annotate(
            dia=TruncDate('fecha_hora')
        ).values('dia').annotate(valor_avg=Avg('valor')).values('dia', 'valor_avg')

        humedad_suelo_promedio = HumedadDeSuelo.objects.filter(planta=planta).annotate(
            dia=TruncDate('fecha_hora')
        ).values('dia').annotate(valor_avg=Avg('valor')).values('dia', 'valor_avg')

        humedad_ambiente_promedio = HumedadDeAmbiente.objects.filter(planta=planta).annotate(
            dia=TruncDate('fecha_hora')
        ).values('dia').annotate(valor_avg=Avg('valor')).values('dia', 'valor_avg')

        data = []
        for item in intensidad_promedio:
            dia = datetime.combine(item['dia'], time.min)
            data.append({
                'dia': dia.isoformat(),
                'planta': planta.nombre,
                'valor': item['valor_avg']
            })

        for item in temperatura_promedio:
            dia = datetime.combine(item['dia'], time.min)
            data.append({
                'dia': dia.isoformat(),
                'planta': planta.nombre,
                'valor': item['valor_avg']
            })

        for item in humedad_suelo_promedio:
            dia = datetime.combine(item['dia'], time.min)
            data.append({
                'dia': dia.isoformat(),
                'planta': planta.nombre,
                'valor': item['valor_avg']
            })

        for item in humedad_ambiente_promedio:
            dia = datetime.combine(item['dia'], time.min)
            data.append({
                'dia': dia.isoformat(),
                'planta': planta.nombre,
                'valor': item['valor_avg']
            })

        return Response(data, status=status.HTTP_200_OK)

class PlantaConsultaView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsultaSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['id']
        user = get_object_or_404(User, id=user_id)
        queryset = Planta.objects.filter(usuario_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)