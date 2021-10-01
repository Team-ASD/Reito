from django.db import models

# Create your models here.

class Reserva(models.Model):
    class Meta:
        unique_together = (('viaje','usuario'),)
        
    viaje = models.ForeignKey("viajes.Viaje", verbose_name="Viaje", null=True, blank=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey("usuarios.Usuario", verbose_name='Pasajero', on_delete=models.CASCADE)
    estado = models.BooleanField(verbose_name="Estado", default=False)

    def __str__(self):
        return str(self.viaje) + " - " + str(self.usuario)
