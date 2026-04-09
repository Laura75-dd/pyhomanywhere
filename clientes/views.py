from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)
from .models import *
from clientes.formularios.cliente_forms import *
from django.db import transaction
from proveedores.formularios.proveedor_forms import *
from clientes.models import Pedido


# IMPORTACIONES DE SEGURIDAD
# LOGINREQUIREDMIXIN
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # PARA CLASES 
from django.contrib.auth.decorators import login_required # PARA FUNCIONES


@login_required(login_url='/')
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    # 1. Busca el pedido exacto
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # 2. Verifica que el pedido sea de este negocio
    if pedido.proyecto == request.user.perfil.proyecto:
        pedido.estado = nuevo_estado
        pedido.save() # Guarda el cambio en la db
        
    return redirect('home')


# ==========================================
# CRUD CLIENTE
# ==========================================
class CreateViewCliente(LoginRequiredMixin, CreateView, UserPassesTestMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear_cliente.html'
    success_url = '/home/'
    login_url = '/' 


    def test_func(self):
        if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.proyecto:
            return False
        if self.request.user.is_superuser:
            return True
        return self.request.user.perfil.rol in ['Administrador', 'Empleado']
    
    def handle_no_permission(self):
        if not hasattr(self.request.user, 'perfil') or not getattr(self.request.user.perfil, 'proyecto', None):
            return render(self.request, 'error_deregistro.html')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        nuevo_cliente = form.save(commit=False)
        nuevo_cliente.proyecto = self.request.user.perfil.proyecto
        nuevo_cliente.save()
        return super().form_valid(form)

# ==========================================
# CRUD PEDIDO
# ==========================================
class CreateViewPedido(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'cliente/crear_pedido.html'
    success_url = '/home/'
    login_url = '/' 

    def test_func(self):
        if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.proyecto:
            return False
        if self.request.user.is_superuser:
            return True
        return self.request.user.perfil.rol in ['Administrador', 'Empleado']

    def handle_no_permission(self):
        if not hasattr(self.request.user, 'perfil') or not getattr(self.request.user.perfil, 'proyecto', None):
            return render(self.request, 'error_deregistro.html')
        return super().handle_no_permission()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        proyecto_actual = self.request.user.perfil.proyecto
        
        # 1. Pasa el proyecto al formulario para filtrar la lista de clientes
        kwargs['proyecto'] = proyecto_actual
        
        # 2. "Pedido"
        # Crea el ticket en memoria y le inyecta los datos ANTES de que Django lo valide
        if kwargs.get('instance') is None:
            kwargs['instance'] = Pedido()
            
        kwargs['instance'].proyecto = proyecto_actual
        kwargs['instance'].vendedor = self.request.user
        
        return kwargs

    def get_context_data(self, **kwargs):
        # Recupera el contexto base (esto ya incluye nuestro 'form' principal)
        data = super().get_context_data(**kwargs)
        proyecto = self.request.user.perfil.proyecto
        
        # Rescatamos el ticket (Pedido) que se está armando en este momento
        pedido_actual = data['form'].instance
        
        # Preparamos el FormSet (las líneas de productos) y las ENLAZAMOS al pedido actual
        if self.request.POST:
            data['detalles'] = DetallePedidoFormSet(
                self.request.POST, 
                instance=pedido_actual,  # Enlaza al ticket correcto
                form_kwargs={'proyecto': proyecto}
            )
        else:
            data['detalles'] = DetallePedidoFormSet(
                instance=pedido_actual,  # Enlaza al ticket correcto
                form_kwargs={'proyecto': proyecto}
            )
        return data
    
    def form_valid(self, form):
        # Rescatamos el contexto que trae nuestro FormSet de productos
        context = self.get_context_data()
        detalles = context['detalles']
        
        # Inyectamos los datos del proyecto y vendedor antes de guardar
        form.instance.proyecto = self.request.user.perfil.proyecto
        form.instance.vendedor = self.request.user

        # Validamos que tanto el pedido (ticket) como los productos sean válidos
        if form.is_valid() and detalles.is_valid():
            # 1. Guardamos el Ticket (Pedido) primero
            self.object = form.save()
            
            # 2. Le decimos al FormSet de productos a qué Ticket pertenecen
            detalles.instance = self.object
            
            # 3. Guardamos los productos en la base de datos
            detalles.save()
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    


    