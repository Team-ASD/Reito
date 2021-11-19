import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reito.settings')
django.setup()

from usuarios.models import Usuario
from django.db.models import Count

correos=Usuario.objects.values('email').annotate(Count('email')).order_by().filter(email__count__gt=1)
usuarios_correo_repetido=[]
for email in correos:
    usuarios_correo_repetido.append(Usuario.objects.filter(email=email['email']))
for usuario in usuarios_correo_repetido:
    usuario.delete()

telefonos=Usuario.objects.values('telefono').annotate(Count('telefono')).order_by().filter(telefono__count__gt=1)
usuarios_telefono_repetido=[]
for telefono in telefonos:
    usuarios_telefono_repetido.append(Usuario.objects.filter(telefono=telefono['telefono']))
for usuario in usuarios_telefono_repetido:
    usuario.delete()