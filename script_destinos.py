import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reito.settings')
django.setup()

from viajes.models import Destino, Viaje
from reservas.models import Reserva

destinos_nuevos=[]
with open('destinos.txt') as d:
    destinos_nuevos=[line.rstrip() for line in d]

destinos_registrados=Destino.objects.all().values("nombre")

destinos_registrados_plano=[]
for destino in destinos_registrados:
    destinos_registrados_plano.append(destino['nombre'])

for destino in destinos_nuevos:
    if destino not in destinos_registrados_plano:
        Destino.objects.create(nombre=destino)

# Reserva.objects.all().delete()
# Viaje.objects.all().delete()