from . import views
from django.urls import path

app_name="usuarios"

urlpatterns = [
    path('signup/', views.NuevoUsuario.as_view(), name="signup"),
    path('login/',views.LoginUsuario.as_view(),name='login'),
    path('logout/',views.LogoutUsuario.as_view(),name='logout'),
    path('mi-cuenta/', views.ver_mi_usuario, name="ver_mi_cuenta"),
    path('editar-cuenta/',views.editar_mi_usuario,name="editar_mi_cuenta"),
    path('ver_info_pasajero/<int:user_pk>/<int:viaje_pk>',views.ver_info_pasajero,name = "ver_info_pas")
]
