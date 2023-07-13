from django.db import models
from apps.SHA.models import HumedadDeAmbiente
from apps.SHS.models import HumedadDeSuelo
from apps.ST.models import Temperatura
from apps.SIL.models import IntensidadDeLuz

class Notificacion(models.Model):
    notificacion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    humedadAmbiente = models.ForeignKey(HumedadDeAmbiente,on_delete=models.CASCADE)
    humedadSuelo = models.ForeignKey(HumedadDeSuelo,on_delete=models.CASCADE)
    temperatura = models.ForeignKey(Temperatura,on_delete=models.CASCADE)
    intensidadLuz = models.ForeignKey(IntensidadDeLuz,on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'ID:{self.notificacion}'
