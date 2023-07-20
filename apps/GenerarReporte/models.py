from django.db import models

class Reporte( models.Model):
    url = models.URLField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
