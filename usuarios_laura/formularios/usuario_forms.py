from django import forms
from usuarios_laura.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__" # Indica que se usaran todos los campos del modelo Usuario

        labels = {   # Sobre escribe los nombres de los campos del modelo por defecto
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'edad': 'Edad',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su edad'}),
        }