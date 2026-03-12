from django import forms
from django.forms import inlineformset_factory
from clientes.models import Cliente, Pedido, DetallePedido
from proyectos.models import Producto 

# ==========================================
# FORMULARIO DE CLIENTE
# ==========================================
class ClienteForm(forms.ModelForm):
    """
    Formulario básico para registrar o editar los datos de un cliente.
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección física'}),
        }

# ==========================================
# FORMULARIO DE PEDIDO (CABECERA)
# ==========================================
class PedidoForm(forms.ModelForm):
    """
    Formulario para la cabecera del pedido. 
    Filtra los clientes para mostrar solo los que pertenecen al proyecto del usuario.
    """
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el proyecto pasado desde la vista
        proyecto = kwargs.pop('proyecto', None)
        super(PedidoForm, self).__init__(*args, **kwargs)
        
        if proyecto:
            # Solo mostramos clientes que pertenezcan a la empresa/proyecto actual
            self.fields['cliente'].queryset = Cliente.objects.filter(proyecto=proyecto)
            self.fields['cliente'].empty_label = "--- Seleccione un Cliente ---"

# ==========================================
# FORMULARIO DE DETALLE (PRODUCTOS)
# ==========================================
class DetallePedidoForm(forms.ModelForm):
    """
    Formulario individual para cada fila de producto en un pedido.
    Filtra los productos por proyecto y asegura que haya stock.
    """
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control item-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control qty-input', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super(DetallePedidoForm, self).__init__(*args, **kwargs)
        
        if proyecto:
            # Solo mostramos productos del catálogo de esta empresa
            self.fields['producto'].queryset = Producto.objects.filter(proyecto=proyecto)
            self.fields['producto'].empty_label = "Seleccionar Producto"

# ==========================================
# FORMSET PARA MANEJO DE VENTAS DINÁMICAS
# ==========================================
# Permite agregar múltiples "DetallePedido" a un solo "Pedido" de forma dinámica.
DetallePedidoFormSet = inlineformset_factory(
    Pedido, 
    DetallePedido, 
    form=DetallePedidoForm,
    extra=1,            # Número de filas vacías que aparecen al inicio
    can_delete=True     # Permite marcar filas para eliminar
)