from . import views
from django.urls import path

app_name="viajes"

urlpatterns = [
    path('nuevo/', views.nuevo_viaje, name="nuevo"),
    path('nuevo-destino/', views.NuevoDestino.as_view(), name="nuevo_destino"),
    path('detalle/<int:pk>', views.detalle_viaje, name="detalle"),
    path('editar/<int:pk>', views.EditarViaje.as_view(), name="editar"),
    path('eliminar/<int:pk>', views.EliminarViaje.as_view(), name="eliminar"),
    path('', views.index, name="index"),
    path('buscar-destinos/', views.buscar_destinos,name="buscar_destinos"),
    path('buscar-viajes/<int:pk>', views.buscar_viajes,name="buscar_viajes"),
    path('ver-viajes/',views.ver_viajes,name = 'ver_viajes'),   
]
