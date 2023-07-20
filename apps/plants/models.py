from django.db import models
from apps.users.models import User

class Planta(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    nombreU = models.CharField('Nombre de Usuario', max_length=100, blank=True)
    humedad = models.IntegerField()
    status = models.BooleanField()

    def save(self, *args, **kwargs):
        self.nombreU = self.usuario.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural ='Plantas'

    def __str__(self):
        return self.nombre
