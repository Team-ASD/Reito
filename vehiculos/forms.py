from django import forms
from .models import Vehiculo


class VehiculosForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = ('modelo', 'marca', 'matricula', 'asientos', 'descripcion')

        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aveo'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chevrolet'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AHF356B'}),
            'asientos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa su auto'}),
        }
        labels = {
            'modelos': 'Modelos',
            'marca': 'Marca',
            'matricula': 'Matrícula',
            'asientos': 'Asientos',
            'descripcion': 'Descripción'
        }
    # This method is in charge of verifying that the length of the license plate is equal to 7
    # and the number of seats is greater than 1.

    def clean(self):
        super(VehiculosForm, self).clean()
        matricula = self.cleaned_data.get('matricula')
        asientos = self.cleaned_data.get('asientos')

        if len(matricula) < 6 or len(matricula) > 7:
            self._errors['matricula'] = self.error_class(
                ['Sólo 6 o 7 caracteres permitidos'])
        
        # Verify if the matricula is alphanumeric
        if not matricula.isalnum():
            self._errors['matricula'] = self.error_class(
                ['Solo caracteres alfanuméricos'])
        
        # Verify if the matricula is in uppercase.
        if not matricula.isupper():
            self._errors['matricula'] = self.error_class(
                ['Solo caracteres en mayúsculas'])

        if asientos < 1:
            self._errors['asientos'] = self.error_class(
                ['Los asientos deben ser un numero entero positivo'])
            
        # Verify the seat number is not greater than 8
        if asientos > 8:
            self._errors['asientos'] = self.error_class(
                ['Solo puedes agregar hasta 8 asientos a tu vehículo.'])


class Vehiculos_editar(forms.ModelForm):
    class Meta:
        model = Vehiculo

        fields = ('descripcion',)

        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa su auto'}),
        }
        labels = {
            'descripcion': 'Descripción'
        }
