from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('nuevo/', views.VehiculoCrear.as_view(), name='nuevo'),
    path('editar/<int:pk>', views.VehiculoActualizar.as_view(), name='editar'),
    path('eliminar/<int:pk>', views.VehiculoEliminar.as_view(), name='eliminar'),
    path('ver/<int:pk>', views.VehiculoDetalle.as_view(), name='ver'),
]
