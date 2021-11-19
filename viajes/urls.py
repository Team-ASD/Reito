from . import views
from django.urls import path

app_name = "viajes"

urlpatterns = [
    path('nuevo/', views.nuevo_viaje, name="nuevo"),
    path('nuevo-destino/', views.NuevoDestino.as_view(), name="nuevo_destino"),
    path('detalle/<int:pk>', views.detalle_viaje, name="detalle"),
    path('eliminar/<int:pk>', views.cancelar_viaje, name="eliminar"),
    path('', views.index, name="index"),
    path('buscar-destinos/', views.buscar_destinos, name="buscar_destinos"),
    path('buscar-viajes/<int:pk>', views.buscar_viajes, name="buscar_viajes"),
    path('ver-viajes/', views.ver_viajes, name='ver_viajes'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('ver-historial/', views.ver_historial, name='ver_historial'),
    path('ver-historial-viajero/', views.ver_historial_viajero, name='ver_historial_viajero'),
    path('ver-historial-conductor/', views.ver_historial_conductor, name='ver_historial_conductor'),
]
