
from vehiculos.models import Vehiculo
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Usuario
from .forms import EditarUsuarioForm, UsuarioForm
from viajes.models import Viaje
from reservas.models import Reserva
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Class implemented to be used as a Signup. This class uses "Usuario" model and its corresponding form.
class NuevoUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "signup.html"
    success_url = reverse_lazy("usuarios:login")

# Class implemented to be used as a Login. This class is utilized to validate user and password of all users when they log in.


class LoginUsuario(LoginView):
    model = Usuario
    template_name = 'login.html'

# Class implemented to logout a user. This class ends the user's actual session on the site.


class LogoutUsuario(LogoutView):
    pass

# Function to see the profile data of the currently logged in user, requires to be logged in.


@login_required
def ver_mi_usuario(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    vehiculo = Vehiculo.objects.filter(id_usuario=usuario).first()
    context = {
        'usuario': usuario,
        'vehiculo': vehiculo
    }
    return render(request, "detalle_usuarios.html", context)


# Function to edit the profile data of the currently logged in user, requires to be logged in.
@login_required
def editar_mi_usuario(request):
    # Search current user.
    user = get_object_or_404(Usuario, id=request.user.id)

    if request.method == "POST":
        # If it is by post, create an instance of the form from the data of the request form and the current user.
        form = EditarUsuarioForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil se ha actualizado")
            return redirect("usuarios:ver_mi_cuenta")
    form = EditarUsuarioForm(instance=user)
    context = {
        "form": form
    }
    return render(request, "editar_usuarios.html", context)


def ver_info_pasajero(request, user_pk, viaje_pk):
    user = get_object_or_404(Usuario, id=user_pk)
    viaje = get_object_or_404(Viaje, id=viaje_pk)
    reserva = get_object_or_404(Reserva, usuario=user, viaje=viaje)
    context = {
        'usuario': user,
        'viaje': viaje,
        'reserva': reserva
    }
    return render(request, 'ver_info_pasajero.html', context)
