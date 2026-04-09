from django import forms
from proyectos.models import *

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
        

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'variante', 'precio', 'disponible']

        labels = {
            'nombre': 'Nombre del Producto',
            'variante': 'Variante (opcional)',
            'precio': 'Precio',
            'disponible': '¿Disponible hoy?',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 
            'placeholder': 'Ej. Pizza de Pepperoni'
            }),
            'variante': forms.TextInput(attrs={'class': 'form-control', 
            'placeholder': 'Ej. Familiar, Individual (opcional)'
            }),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 
            'placeholder': 'Ej. 150.00'
            }),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['insumo', 'cantidad_actual', 'unidad_medida', 'stock_minimo']

        labels = {
            'insumo': 'Nombre del Insumo',
            'cantidad_actual': 'Cantidad',
            'unidad_medida': 'Unidad de Medida',
            'stock_minimo': 'Stock Mínimo',
        }

        widgets = {
            'insumo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Tortillas'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 50'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. piezas, kg, litros'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 10'}),
        }