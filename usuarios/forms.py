from django import forms
from .models import Usuario

# Form that represents the registration data of a user.


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'telefono', 'foto'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': "Nombre(s)",
            'last_name': 'Apellidos',
            'email': 'Correo',
            'password': 'Contraseña',
            'telefono': 'Teléfono',
            'foto': 'Fotografía'
        }
        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Form that represents the data that a user can edit about himself.


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'telefono', 'descripcion', 'foto')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Hablanos de tí'})
        }

        labels = {
            'username': 'Nombre de usuario',
            'first_name': "Nombre(s)",
            'last_name': 'Apellidos',
            'email': 'Correo',
            'telefono': 'Teléfono',
            'descripcion': 'Descripción',
            'foto': 'Fotografía'
        }
