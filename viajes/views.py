from django.contrib import messages
from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from .models import Viaje, Destino
from vehiculos.models import Vehiculo
from reservas.models import Reserva
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import DestinoForm, ViajeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.core.paginator import Paginator

from datetime import datetime


def index(request):
    # Here are the most frequent destinations to show them in the Home
    destinos = obtener_destinos_frecuentes()
    viajes_recientes=obtener_ultimos_reitos()
    context = {
        'destinos': destinos,
        "viajes_recientes":viajes_recientes}
    return render(request, 'index.html', context=context)


class NuevoViaje(LoginRequiredMixin, CreateView):
    model = Viaje
    template_name = "nuevo.html"
    form_class = ViajeForm
    success_url = reverse_lazy('viajes:index')

    def form_valid(self, form):
        usuario = get_object_or_404(Usuario, id=self.request.user.id)
        form.instance.conductor = usuario
        return super().form_valid(form)


@login_required
def nuevo_viaje(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    vehiculos = Vehiculo.objects.filter(id_usuario=request.user.id)
    asientos_publicados = 0
    
    # Validation to verify if the user has a vehicle registered
    if vehiculos:
    
        asientos_publicados = vehiculos[0].asientos
        if request.method == "POST":
            if (vehiculos.count() > 0):
                form = ViajeForm(request.POST)
                form.instance.conductor = usuario
                capacidad = int(form.data['asientos'])
                
                # Here it is validated that the number of seats registered in the vehicle is not greater than the one entered in the form
                if capacidad > asientos_publicados:
                    #The error is added to the form to the 'asientos' field
                    form.add_error('asientos',[f'El número de asientos es mayor a la capacidad de tu vehiculo.\nTu capacidad es de {asientos_publicados} asientos. '])
                    messages.error(request, "Los datos ingresados no son válidos.")
                    return render(request,'nuevo.html',context={'form':form,
                                                                'tiene_vehiculo': vehiculos,
                                                                "asientos_v":asientos_publicados,})
                
                if form.is_valid():
                    form.save()
                    messages.success(request, "Se ha creado con éxito tu viaje.")
                    return redirect('viajes:ver_viajes')
                else:
                    messages.error(request, "Los datos ingresados no son válidos.")
                    return render(request,'nuevo.html',context={'form':form,
                                                                'tiene_vehiculo': vehiculos,
                                                                "asientos_v":asientos_publicados
                                                                })
            else:
                messages.error(
                    request, "Aun no tienes un vehículo para realizar el viaje.")
                return redirect('viajes:nuevo')
            
        form = ViajeForm()
        context = {
            "form": form,
            "asientos_v":asientos_publicados,
            "tiene_vehiculo" : True
        }
        return render(request, "nuevo.html", context)
    else:
        form = ViajeForm()
        context = {
            "tiene_vehiculo" : False,
            "form" : form
        }
        return render(request, "nuevo.html", context)
        
class NuevoDestino(LoginRequiredMixin, CreateView):
    model = Destino
    # extra_context = {'':''}
    form_class = DestinoForm
    template_name = "nuevo_destino.html"
    success_url = reverse_lazy('viajes:nuevo')


@login_required
def detalle_viaje(request, pk):
    # get the reito with the given pk
    viaje = get_object_or_404(Viaje, id=pk)
    
    # get the user driver
    usuario = get_object_or_404(Usuario, id=viaje.conductor.id)

    if(request.user.id == usuario.id):
        reservas = Reserva.objects.filter(viaje=viaje).exclude(estado=False)
        viajeros = []

        for reserva in reservas:
            viajero = Usuario.objects.get(id=reserva.usuario.id)
            viajeros.append(viajero)

        reservas_pendientes = Reserva.objects.filter(
            viaje=viaje).exclude(estado=True)

        posibles_viajeros = []

        for reserva in reservas_pendientes:
            viajero = Usuario.objects.get(id=reserva.usuario.id)
            posibles_viajeros.append(viajero)

        context = {
            'viaje': viaje,
            'viajeros': viajeros,
            'viajeros_pendientes': posibles_viajeros
        }
        return render(request, "detalle_viaje.html", context)

    else:
        # Traveler travel detail
        reservas = Reserva.objects.filter(
            usuario=request.user.id, viaje=pk).first()
        context = {}
        
        # get the vehicle from the user driver
        vehiculo = Vehiculo.objects.filter(id_usuario=usuario).first()
        
        if vehiculo:
            context['vehiculo'] = vehiculo
        if(reservas):
            # Send the reservation state
            context['estado_reserva'] = reservas.estado
            context['tiene_reserva'] = True
            
            if(reservas.estado == True):
                context['telefono'] = usuario.telefono
        context['viaje'] = viaje
        # Sends user's image to the frontend
        context['foto'] = usuario.foto
        context['descripcion'] = usuario.descripcion

        return render(request, "detalle_viaje_viajero.html", context)

@login_required
def cancelar_viaje(request, pk):
    # Get an instance of the trip you want to cancel.
    viaje = get_object_or_404(Viaje, id=pk, conductor=request.user)

    # Verify that it comes through a form.
    if request.method == "POST":
        # Validation of not being able to cancel a trip that has a date already made.
        # Obtaining current dates and corresponding to the trip.
        fecha = viaje.fecha
        hora = viaje.hora
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()
        # Cancel if it is older than the recent date.
        if fecha > fecha_actual:
            viaje.delete()
            messages.success(request, "Tu viaje se ha cancelado con éxito.")
            return redirect('viajes:ver_viajes')
            # If it is the same date but it is not yet time for the trip.
        elif fecha == fecha_actual and hora > hora_actual:
            viaje.delete()
            messages.success(request, "Tu viaje se ha cancelado con éxito.")
            return redirect('viajes:ver_viajes')
            # If the date of the trip has passed, it does not allow canceling and sends an error message.
        else:
            messages.error(
                request, "Este viaje no puede ser cancelado porque ya pasó su fecha de realización.")
            return redirect('viajes:detalle', pk=pk)


# Method in charge of retrieving the list of destinations that match what the user types in the search bar.
# What is written in the search bar is sent here and the possible destinations are returned.
@login_required
def buscar_destinos(request):
    destino = request.GET.get('destino')
    destinos = []
    if destino:
        destinos_encontrados = Destino.objects.filter(
            nombre__icontains=destino).values("id", "nombre")
        for d in destinos_encontrados:
            destinos.append(d)
    return JsonResponse({'status': 200, 'data': destinos})

# Method in charge of recovering trips based on a unique identifier of the destination.
# This method also filters trips based on price.
@login_required
def buscar_viajes(request, pk):
    destino_encontrado = get_object_or_404(Destino, id=pk)
    if request.GET.get('precio'):
        lista_viajes = Viaje.objects.filter(
                                    destino=destino_encontrado, 
                                    precio__lte=request.GET.get('precio'))
    else:
        lista_viajes = Viaje.objects.filter(destino=destino_encontrado)
   
    # Unfinished trips are filtered here
    viajes_recientes = []
    for viaje in lista_viajes:
        # First check that if there is a trip on the current day
        # if there is, then validate that the time is greater than the current one
        # and if these two conditions are correct it is added to the list of recent trips.
        if viaje.fecha == datetime.now().date():
            if viaje.hora > datetime.now().time():
                viajes_recientes.append(viaje)
        # Then we only verify the days older than the current one to add them to the
        # viajes_recientes list.
        if viaje.fecha > datetime.now().date():
            viajes_recientes.append(viaje)
           
    viajes = []
    for viaje in viajes_recientes:
        if viaje.asientos > 0:
            viajes.append(viaje)

    context = {
        "destino": destino_encontrado,
    }
    
    if(len(viajes) > 0):
        context['viajes'] = viajes
    if request.GET.get('precio'):
        context['precio'] = request.GET.get('precio')
        
    return render(request, "lista_viajes.html", context)

# Method to get the list of travels made by the user and currently available
@login_required
def ver_viajes(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    viajes = Viaje.objects.filter(conductor=usuario)
    # Here unfinished trips are filtered
    viajes_recientes = []
    for viaje in viajes:
        # First check that if there is a trip on the current day
        # yes, if there is after, it validates that the time is greater than the current one
        # and if these two conditions are correct it is added to the list of recent trips.
        if viaje.fecha == datetime.now().date():
            if viaje.hora > datetime.now().time():
                viajes_recientes.append(viaje)
        # Then we only verify the days older than the current one to add them to the
        # list of recent trips.
        if viaje.fecha > datetime.now().date():
            viajes_recientes.append(viaje)
            
    context = {
        'viajes': viajes_recientes
    }
    return render(request, 'ver_viajes.html', context)


@login_required
def mis_reservas(request):
    # Get current user and date data.
    usuario = get_object_or_404(Usuario, id=request.user.id)
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    # Get all reservations, past and current.
    reservas_general = Reserva.objects.filter(usuario=usuario)
    reservas = []
    # For to filter past reservations from general ones.
    for reserva in reservas_general:
        viaje = reserva.viaje
        if viaje.fecha > fecha_actual:
            reservas.append(reserva)
        elif viaje.fecha == fecha_actual and viaje.hora > hora_actual:
            reservas.append(reserva)

    context = {
        'reservas': reservas
    }
    return render(request, 'mis_reservas.html', context)

'''
Función que obtiene los destinos mas frecuentes o populares.
'''


def obtener_destinos_frecuentes():
    resultado = (Viaje.objects
                 .values('destino_id')
                 # It is the column to be counted.
                 .annotate(contador=Count('destino_id'))
                 # Sort by counter and only get the first 5 results.
                 .order_by('-contador')[:5]
                 )

    destinos = []
    # Obtains each Destination from the previous result and saves them in a list.
    for item in resultado:
        destino = get_object_or_404(Destino, id=item['destino_id'])
        destinos.append(destino)

    return destinos

# Method utilized to get the 3 most recent Reitos.
def obtener_ultimos_reitos():
    lista_viajes=Viaje.objects.values('id').order_by('-id')[:3] # We get the latest 3 Reitos from our DB.
    viajes_recientes=[]
    for viaje in lista_viajes:
        viaje=get_object_or_404(Viaje, id=viaje['id'])
        # First check that if there is a trip on the current day
        # if there is, then validate that the time is greater than the current one
        # and if these two conditions are correct it is added to the list of recent trips.
        if viaje.fecha == datetime.now().date():
            if viaje.hora > datetime.now().time():
                viajes_recientes.append(viaje)
        # Then we only verify the days older than the current one to add them to the
        # viajes_recientes list.
        if viaje.fecha > datetime.now().date():
            viajes_recientes.append(viaje)
    return viajes_recientes

# Function to get the past trips and reservations of the logged in user.
@login_required
def ver_historial(request):
    # Get current user and date data.
    usuario = get_object_or_404(Usuario, id=request.user.id)
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    # Get all reservations, past and current.
    reservas_general = Reserva.objects.filter(usuario=usuario)
    reservas = []
    # For to filter past reservations from general ones.
    for reserva in reservas_general:
        viaje = reserva.viaje
        if viaje.fecha < fecha_actual:
            reservas.append(reserva)
        elif viaje.fecha == fecha_actual and viaje.hora < hora_actual:
            reservas.append(reserva)
    
    # Get general, past and current trips.
    viajes_general = Viaje.objects.filter(conductor=usuario)
    viajes = []
    # For to filter the past trips of the generals.
    for viaje in viajes_general:
        if viaje.fecha < fecha_actual:
            viajes.append(viaje)
        elif viaje.fecha == fecha_actual and viaje.hora < hora_actual:
            viajes.append(viaje)
    # Add in the context that will go to the front the lists of
    # Past trips and reservations.
    context = {
        'reservas': reservas,
        'viajes': viajes,
        'viajero' : True,
        'conductor' : True
    }
    return render(request, 'ver_historial.html', context)

def ver_historial_viajero(request):
    # Get current user and date data.
    usuario = get_object_or_404(Usuario, id=request.user.id)
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    # Get all reservations, past and current.
    reservas_general = Reserva.objects.filter(usuario=usuario)
    reservas = []
    # For to filter past reservations from general ones.
    for reserva in reservas_general:
        viaje = reserva.viaje
        if viaje.fecha < fecha_actual:
            reservas.append(reserva)
        elif viaje.fecha == fecha_actual and viaje.hora < hora_actual:
            reservas.append(reserva)
                
    context = {
        'reservas': reservas,
        'viajero' : True
    }
        
    return render(request, 'ver_historial.html', context)

def ver_historial_conductor(request):
    # Obtener usuario y datos de fecha actuales.
    usuario = get_object_or_404(Usuario, id=request.user.id)
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    # Get general, past and current trips.
    viajes_general = Viaje.objects.filter(conductor=usuario).order_by('-fecha')
    viajes = []
    # For to filter the past trips of the generals.
    for viaje in viajes_general:
        if viaje.fecha < fecha_actual:
            viajes.append(viaje)
        elif viaje.fecha == fecha_actual and viaje.hora < hora_actual:
            viajes.append(viaje)
            
    context = { 
        'viajes': viajes,
        'conductor' : True
    }
    return render(request, 'ver_historial.html', context) 