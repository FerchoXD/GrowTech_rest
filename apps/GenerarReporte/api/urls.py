from django.urls import path
from ..views import GenerarReporteTemperaturaView,GenerarReporteIntensidadView,GenerarReporteHumedadAmbienteView,GenerarReporteHumedadSueloView

urlpatterns = [
    path('reporte/semanal/temperatura/', GenerarReporteTemperaturaView.as_view(), name='Generar-Reporte-Semanal-temperatura'),
    path('reporte/semanal/intensidad/', GenerarReporteIntensidadView.as_view(), name='Generar-Reporte-Semanal-intensidad'),
    path('reporte/semanal/Humedad/ambiente/', GenerarReporteHumedadAmbienteView.as_view(), name='Generar-Reporte-Semanal-Humedad-ambiente'),
    path('reporte/semanal/Humedad/suelo/', GenerarReporteHumedadSueloView.as_view(), name='Generar-Reporte-Semanal-Humedad-suelo'),
]