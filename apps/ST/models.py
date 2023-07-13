from django.db import models
from apps.plants.models import Planta

class Temperatura(models.Model):
    valor = models.IntegerField()
    fecha_hora = models.DateField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE,default=1)

    class Meta:
        verbose_name = 'Temperatura'
        verbose_name_plural = 'Temperaturas'
    
    def __str__(self):
        return f'ID:{self.id}, valor:{self.valor}, fecha_hora:{self.fecha_hora}'

