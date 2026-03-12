from django import forms
from proyectos.models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        
        # En lugar de "__all__", definE que ve el usuario.
        fields = ['nombre', 'descripcion', 'dias_de_venta'] 

        labels = {
            'nombre': 'Nombre del Negocio / Proyecto',
            'descripcion': 'Descripción breve',
            'dias_de_venta': 'Días de Operación',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 
            'placeholder': 'Ej. Taquería Los Compadres'
            }),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 
            'placeholder': '¿De qué trata tu negocio?', 
            'rows': 3
            }),
            'dias_de_venta': forms.TextInput(attrs={'class': 'form-control', 
            'placeholder': 'Ej. Lunes a Viernes, de 9am a 5pm'
            }),
        }
        