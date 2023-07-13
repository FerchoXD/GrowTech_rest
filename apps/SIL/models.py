from django.db import models
from apps.plants.models import Planta

class IntensidadDeLuz(models.Model):
    valor = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE,default=1)

    class Meta:
        verbose_name = 'Intensidad de Luz'
        verbose_name_plural = 'Intensidades de Luz'

    def __str__(self):
        return f'ID:{self.id}, valor: {self.valor}, fecha_hora: {self.fecha_hora}'
