from django.db import models
from apps.users.models import User

class Planta(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    nombreU = User.username
    humedad = models.IntegerField()
    status = models.BooleanField()

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural ='Plantas'

    def __str__(self):
        return self.nombre
