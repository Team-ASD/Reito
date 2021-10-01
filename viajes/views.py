from django.contrib import messages
from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from .models import Viaje, Destino
from reservas.models import Reserva
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import JsonResponse, request
from django.core import serializers
from django.urls import reverse_lazy
from .forms import DestinoForm, ViajeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'index.html')

class NuevoViaje(LoginRequiredMixin, CreateView):
    model = Viaje
    template_name="nuevo.html"
    form_class = ViajeForm
    success_url = reverse_lazy('viajes:index')
    
    def form_valid(self, form):
        usuario = get_object_or_404(Usuario, id=self.request.user.id)
        form.instance.conductor = usuario
        return super().form_valid(form)

@login_required
def nuevo_viaje(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    if request.method == "POST":
        vehiculos = Vehiculo.objects.filter(id_usuario = request.user.id)
        if (vehiculos.count() > 0):
            form = ViajeForm(request.POST)
            form.instance.conductor = usuario

            capacidad = int(form.data['asientos'])
            asientos_publicados = vehiculos[0].asientos

            if form.is_valid() and asientos_publicados >= capacidad:
                form.save()
                messages.success(request, "Se ha creado con exito tu viaje.")
                return redirect('viajes:index')
            else:
                messages.error(request, "Los datos ingresados no son validos")
                return redirect('viajes:nuevo')
        else:
            messages.error(request, "Aun no tienes un vehiculo para realizar el viaje")
            return redirect('viajes:nuevo')

    form = ViajeForm()
    context = {
        "form":form
    }
    return render(request, "nuevo.html", context)

class NuevoDestino(LoginRequiredMixin, CreateView):
    model = Destino
    #extra_context = {'':''}
    form_class = DestinoForm
    template_name = "nuevo_destino.html"
    success_url = reverse_lazy('viajes:nuevo')

@login_required
def detalle_viaje(request, pk):
    viaje = get_object_or_404(Viaje, id=pk)
    usuario = get_object_or_404(Usuario, id=viaje.conductor.id)

    if(request.user.id == usuario.id):
        reservas = Reserva.objects.filter(viaje = viaje).exclude(estado = False)
        viajeros = []

        for reserva in reservas:
            viajero = Usuario.objects.get(id=reserva.usuario.id)
            viajeros.append(viajero)

        reservas_pendientes = Reserva.objects.filter(viaje = viaje).exclude(estado = True)

        posibles_viajeros = []

        for reserva in reservas_pendientes:
            viajero = Usuario.objects.get(id=reserva.usuario.id)
            posibles_viajeros.append(viajero)

        context={
            'viaje':viaje,
            'viajeros':viajeros,
            'viajeros_pendientes':posibles_viajeros
        }
        return render(request, "detalle_viaje.html", context)

    else:
        reservas = Reserva.objects.filter(usuario=request.user.id, viaje=pk).first()
        context = {}
        if(reservas):
            context['tiene_reserva']=True
            if(reservas.estado):
                context['telefono']=usuario.telefono
        context['viaje'] = viaje
        return render(request, "detalle_viaje_viajero.html", context)

class EditarViaje(LoginRequiredMixin, UpdateView):
    model = Viaje
    form_class = ViajeForm
    #extra_context = {'':''}
    success_url = reverse_lazy('viajes:detalle')

class EliminarViaje(LoginRequiredMixin,DeleteView):
    model = Viaje
    success_url = reverse_lazy('viajes:nuevo')

@login_required
def buscar_destinos(request):
    destino=request.GET.get('destino')
    destinos=[]
    if destino:
        destinos_encontrados=Destino.objects.filter(nombre__icontains=destino).values("id","nombre")
        for d in destinos_encontrados:
            destinos.append(d)
    return JsonResponse({'status' : 200 , 'data' : destinos})

@login_required
def buscar_viajes(request, pk):
    destino_encontrado=get_object_or_404(Destino,id=pk)
    lista_viajes=Viaje.objects.filter(destino=destino_encontrado)
    viajes=[]
    for viaje in lista_viajes:
        if viaje.asientos>0:
            viajes.append(viaje)
    context={
        "destino":destino_encontrado
    }
    if(len(viajes)>0):
        context['viajes']=viajes
    return render(request,"lista_viajes.html",context)

@login_required
def ver_viajes(request):
    usuario = get_object_or_404(Usuario,id = request.user.id)
    reservas = Reserva.objects.filter(usuario=usuario)
    viajes = Viaje.objects.filter(conductor = usuario)
    context = {
        'reservas':reservas,
        'viajes':viajes
    }
    return render(request, 'ver_viajes.html',context)
