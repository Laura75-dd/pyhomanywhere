from django import forms
from django.contrib.auth.models import User
from perfiles.models import Perfil

class PerfilForm(forms.ModelForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Perfil
        fields = ['telefono', 'rol', 'puesto', 'puesto_personalizado']
        
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
            'puesto_personalizado': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que pasamos desde la vista
        self.user_creador = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        
        # Filtro de seguridad para Roles
        # Si no es superusuario, quitamos Admin y Empleado global
        if self.user_creador and not self.user_creador.is_superuser:
            if 'rol' in self.fields:
                choices_actuales = self.fields['rol'].choices
                # Solo permitimos roles operativos (ajusta los nombres exactos de tu BD)
                roles_prohibidos = ['Administrador', 'Empleado']
                nuevas_choices = [c for c in choices_actuales if c[0] not in roles_prohibidos]
                self.fields['rol'].choices = nuevas_choices

    def save(self, commit=True, proyecto_asignado=None):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"]
        )
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()

        perfil = super().save(commit=False)
        perfil.usuario = user

        if proyecto_asignado:
            perfil.proyecto = proyecto_asignado

        if commit:
            perfil.save()
            
        return perfil