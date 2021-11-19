from django import forms
from .models import Viaje, Destino
from datetime import datetime

# Personalized field for DateInput field.

class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)
        
class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje

        fields = 'destino', 'fecha','hora', 'asientos', 'precio', 'descripcion'

        widgets = {
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'fecha': DateInput(format=["%d-%m-%Y"],attrs ={'class':'form-control'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM (Formato de 24 horas)','type': 'time'}),
            'asientos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de acuerdo a tu vehículo.', 'min': '1'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '999.99', 'min': '0','type':'number','pattern':'[0-9]+'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe detalles de tu viaje aquí.'}),
        }
    # Method that validates that the date and time are not passed
    def clean(self):
        super(ViajeForm,self).clean()
        fecha = self.cleaned_data.get('fecha')
        hora = self.cleaned_data.get('hora')
        # It validates that if it is the current date and then it validates that the current 
        # time is not less, if this happens it saves the error and shows it.
        if datetime.now().date() == fecha:
            if hora < datetime.now().time():
                self._errors['hora']= self.error_class(['La hora ingresada no es válida, ingresa una hora mayor a la actual.'])
        #Validate that if the current date is not less than the one entered, if this happens it saves the error and displays it.
        if fecha < datetime.now().date():
            self._errors['fecha']= self.error_class(['La fecha ingresada no es valida, ingresa una fecha mayor o igual a la actual.'])



class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino

        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del nuevo destino.'})
        }
