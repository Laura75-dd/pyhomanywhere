from django import forms
from proveedores.models import *

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        # Define los campos 
        fields = ['nombre', 'tipo', 'telefono', 'email', 'direccion'] 

        labels = { 
            'nombre': 'Nombre de la Empresa o Contacto',
            'direccion': 'Dirección',
            'telefono': 'Número de Teléfono',
            'tipo': '¿Qué te surten? (Ej. Lácteos, Empaques)',
            'email': 'Correo Electrónico',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Empaques Bio'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Desechables'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle y número'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 dígitos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contacto@empresa.com'}),
        }
        
# ==========================================
# FORMULARIO: REGISTRAR COMPRA DE INSUMO
# ==========================================
class CompraInsumoForm(forms.ModelForm):
    class Meta:
        model = CompraInsumo
        # pide al cajero/dueño los datos de la nota de compra
        fields = ['proveedor', 'nombre_insumo', 'cantidad', 'costo_unitario']

        labels = {
            'proveedor': 'Selecciona el Proveedor',
            'nombre_insumo': '¿Qué compraste? (Insumo)',
            'cantidad': 'Cantidad (Ej. 5)',
            'costo_unitario': 'Costo por unidad ($)',
        }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'nombre_insumo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cajas de Tomate'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej. 150.50'}),
        }
    
    def __init__(self, *args, **kwargs):
        # 1. Extrae el proyecto que le manda desde la vista
        proyecto_actual = kwargs.pop('proyecto', None)
        super(CompraInsumoForm, self).__init__(*args, **kwargs)
        
        # 2. Si recibe un proyecto, filtra la lista desplegable de proveedores
        if proyecto_actual:
            self.fields['proveedor'].queryset = Proveedor.objects.filter(proyecto=proyecto_actual)
            self.fields['proveedor'].empty_label = " Elige un proveedor "