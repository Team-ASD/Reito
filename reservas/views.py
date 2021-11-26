from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from usuarios.models import Usuario
from viajes.models import Viaje
from datetime import datetime
from .models import Reserva
from django.contrib.auth.decorators import login_required


@login_required
def nueva_reserva(request, user_pk, viaje_pk):

    if(user_pk and viaje_pk):
        viaje = Viaje.objects.get(id=viaje_pk)
        
        # Validation of not being able to make a reservation in a passed trip.
        # Obtaining current dates and corresponding to the trip.
        fecha = viaje.fecha
        hora = viaje.hora
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()
        
        # Validate that the time and date is bigger than the current date and time.
        if fecha < fecha_actual or fecha==fecha_actual and hora<hora_actual:
            messages.error(request, "No puedes en éste viaje")
            return redirect('viajes:index')


        usuario = Usuario.objects.get(id=user_pk)
        conductor = get_object_or_404(Usuario, id=viaje.conductor.id)


        if(conductor.id == request.user.id):
            messages.error(request, "No puedes reservar en tu propio viaje")
            return redirect('viajes:index')

        if(viaje.asientos > 0):
            try:
                reserva = Reserva.objects.create(viaje=viaje, usuario=usuario)
                reserva.save()
                messages.warning(
                    request, "Tu solicitud se envió exitosamente")
                return redirect('viajes:index')
            except:
                messages.error(request, "No se pudo reservar tu asiento")
                return redirect('viajes:index')
        else:
            messages.error(
                request, "Ya no hay asientos disponibles en este viaje")
            return redirect('viajes:index')


@login_required
def cancelar_reserva(request, user_pk, viaje_pk):
    if(user_pk and viaje_pk):
        reserva = get_object_or_404(Reserva, usuario=user_pk, viaje=viaje_pk)
        viaje = get_object_or_404(Viaje, id=viaje_pk)
        
        # Get the date and time of the Reito 
        fecha = viaje.fecha
        hora = viaje.hora
        # Get the current date and time
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()
        
        if (fecha > fecha_actual) or (fecha == fecha_actual and hora > hora_actual):
            if(reserva and viaje):
                if(reserva.estado):
                    viaje.asientos += 1
                    viaje.save()
                    reserva.delete()
                    messages.success(request, "Has cancelado tu reserva")
                    return redirect('viajes:index')
                else:
                    reserva.delete()
                    messages.success(request, "Has cancelado tu reserva")
                    return redirect('viajes:index')
            else:
                messages.error(request, "No fue posible cancelar la reserva")
                return redirect('viajes:index')
        else:
            messages.error(request, "Esta reserva no puede ser cancelada porque ya pasó su fecha de realización.")
            return redirect('viajes:index')


@login_required
def aceptar_reserva(request, user_pk, viaje_pk):
    viaje = Viaje.objects.get(id=viaje_pk)
    usuario = Usuario.objects.get(id=user_pk)
    reserva = Reserva.objects.get(viaje=viaje, usuario=usuario)
    reserva.estado = True
    reserva.save()
    viaje.asientos -= 1
    viaje.save()
    messages.success(request, "Pasajero aceptado correctamente")
    return redirect('viajes:detalle', pk=viaje.id)
