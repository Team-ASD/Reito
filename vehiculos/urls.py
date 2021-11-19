from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('nuevo/', views.VehiculoCrear.as_view(), name='nuevo'),
    path('editar/', views.editar_vehiculo, name='editar'),
    path('eliminar/<int:pk>', views.eliminar_vehiculo, name='eliminar'),
    path('ver/', views.ver_vehiculo, name='ver'),
]
