from . import views
from django.urls import path

app_name="reservas"

urlpatterns = [
    path('nueva/<int:user_pk>/<int:viaje_pk>', views.nueva_reserva, name="nueva"),
    path('cancelar/<int:user_pk>/<int:viaje_pk>', views.cancelar_reserva, name="cancelar"),
    path('aceptar-reserva/<int:user_pk>/<int:viaje_pk>',views.aceptar_reserva,name="aceptar")
]