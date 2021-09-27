from usuarios.models import Usuario
from .models import Viaje, Destino
from reservas.models import Reserva
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse_lazy
from .forms import DestinoForm, ViajeForm

def index(request):
    return render(request, 'index.html')

class NuevoViaje(CreateView):
    model = Viaje
    #extra_context = {'':''}
    template_name="nuevo.html"
    form_class = ViajeForm
    success_url = reverse_lazy('viajes:index')

    def form_valid(self, form):
        usuario = get_object_or_404(Usuario, id=self.request.user.id)
        form.instance.conductor = usuario
        return super().form_valid(form)

class NuevoDestino(CreateView):
    model = Destino
    #extra_context = {'':''}
    form_class = DestinoForm
    success_url = reverse_lazy('viajes:detalle_destino')

def detalle_viaje(request, pk):
    viaje = get_object_or_404(Viaje, id=pk)

    reservas = Reserva.objects.filter(viaje = viaje).exclude(estado = False)

    viajeros = []

    for reserva in reservas:
        viajero = Usuario.objects.get(id=reserva.usuario.id)
        viajeros.append(viajero)

    context={
        'viaje':viaje,
        'viajeros':viajeros
    }
    return render(request, "detalle_viaje.html", context)

class EditarViaje(UpdateView):
    model = Viaje
    form_class = ViajeForm
    #extra_context = {'':''}
    success_url = reverse_lazy('viajes:detalle')

class EliminarViaje(DeleteView):
    model = Viaje
    success_url = reverse_lazy('viajes:nuevo')

class DetalleViajeViajero(DetailView):
    model = Viaje
    template_name="detalle_viaje_viajero.html"

    def get_context_data(self, **kwargs):
        context = super(DetalleViajeViajero,self).get_context_data(**kwargs)
        reservas = Reserva.objects.filter(usuario=self.request.user.id, viaje=self.kwargs.get('pk'))
        if(reservas):
            context['tiene_reserva'] = True
        return context

def buscar_destinos(request):
    destino=request.GET.get('destino')
    destinos=[]
    if destino:
        destinos_encontrados=Destino.objects.filter(nombre__icontains=destino).values("id","nombre")
        for d in destinos_encontrados:
            destinos.append(d)
    return JsonResponse({'status' : 200 , 'data' : destinos})

def buscar_viajes(request, pk):
    destino_encontrado=get_object_or_404(Destino,id=pk)
    lista_viajes=Viaje.objects.filter(destino=destino_encontrado)
    viajes=[]
    for viaje in lista_viajes:
        reservas=len(Reserva.objects.filter(viaje=viaje.id))
        if viaje.asientos-reservas>0:
            viajes.append(viaje)
    context={
        "destino":destino_encontrado
    }
    if(len(viajes)>0):
        context['viajes']=viajes
    
    return render(request,"lista_viajes.html",context)

