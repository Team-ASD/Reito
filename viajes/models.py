from django.db import models
from datetime import date

from django.db.models.fields import CharField, DecimalField, IntegerField


class Destino(models.Model):
    nombre = models.CharField("Nombre", max_length=200)

    def __str__(self):
        return self.nombre


class Viaje(models.Model):
    conductor = models.ForeignKey(
        "usuarios.Usuario", verbose_name="Conductor", null=True, blank=True, on_delete=models.CASCADE)
    destino = models.ForeignKey(
        "viajes.Destino", verbose_name='Destino', on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name="Fecha", default=date.today)
    hora = models.TimeField(verbose_name="Hora", auto_now=False, auto_now_add=False)
    asientos = IntegerField('Asientos')
    precio = DecimalField('Precio', max_digits=5, decimal_places=2)
    descripcion = CharField('Descripción', max_length=500)

    def __str__(self):
        return self.destino
