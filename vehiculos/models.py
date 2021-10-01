from django.db import models
from usuarios.models import Usuario

class Vehiculo(models.Model):
    modelo = models.CharField("Modelo", max_length=20)
    marca = models.CharField("Marca", max_length=20)
    matricula = models.CharField("Matricula", max_length=7)
    asientos = models.IntegerField("Asientos")
    descripcion = models.CharField("Descripcion", max_length=500)
    id_usuario = models.OneToOneField("usuarios.Usuario",verbose_name="Usuario", on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.matricula
# Create your models here.
