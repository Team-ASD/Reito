from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Viaje, Destino

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje

        fields = 'destino', 'fecha', 'hora', 'asientos', 'precio', 'descripcion'

        widgets = {
            'destino':forms.Select(attrs={'class':'form-control'}),
            'fecha':forms.DateInput(attrs={'class':'form-control'}),
            'hora':forms.TimeInput(attrs={'class':'form-control', 'placeholder':'HH:MM (Formato de 24 horas)'}),
            'asientos':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número de acuerdo a tu vehiculo.'}),
            'precio':forms.NumberInput(attrs={'class':'form-control','placeholder':'999.99'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','placeholder':'Describe detalles de tu viaje aquí.'}),
        }

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        
        fields = '__all__'

        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del nuevo destino.'})
        }
