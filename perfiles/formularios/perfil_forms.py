from django import forms
from django.contrib.auth.models import User
from perfiles.models import Perfil

class PerfilForm(forms.ModelForm):
    # Campos que van hacia el modelo nativo User
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juanperez'}))
    first_name = forms.CharField(label='Nombre(s)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Perfil
        # Aquí conservamos el teléfono, el puesto y tu campo personalizado
        fields = ['telefono', 'puesto', 'puesto_personalizado'] 
        
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Será su contraseña inicial'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
            'puesto_personalizado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique el puesto...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user_creador = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, proyecto_asignado=None):
        # 1. Generamos un correo falso obligatorio para Django
        username_limpio = self.cleaned_data["username"].lower().replace(" ", "")
        email_generado = f"{username_limpio}@smartdayz.local"

        # 2. Creamos el usuario base
        user = User(
            username=username_limpio,
            email=email_generado,
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"]
        )
        
        # 3. Usamos el teléfono como contraseña inicial
        telefono = self.cleaned_data.get("telefono")
        password_inicial = telefono if telefono else f"{username_limpio}123"
        user.set_password(password_inicial)
        
        if commit:
            user.save()

        # 4. Creamos el Perfil y guardamos los puestos tal como los diseñaste
        perfil = super().save(commit=False)
        perfil.usuario = user
        perfil.rol = 'Empleado'  # El rol se pone automático para que el Admin no trabaje de más

        if proyecto_asignado:
            perfil.proyecto = proyecto_asignado

        if commit:
            perfil.save()
            
        return perfil