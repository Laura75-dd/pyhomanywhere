from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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

# IMPORTACIONES DE SEGURIDAD
# LOGINREQUIREDMIXIN
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # PARA CLASES
from django.contrib.auth.decorators import login_required # PARA FUNCIONES


@login_required(login_url='/')
def home(request):
    if not hasattr(request.user, 'perfil') or not request.user.perfil.proyecto:
        return render(request, 'error_deregistro.html')
        
    context = {
        'mensaje': f'Gestión de Clientes y Ventas - {request.user.perfil.proyecto.nombre}',
        "user": request.user
    }
    return render(request, 'index.html', context)

# ==========================================
# CRUD CLIENTE
# ==========================================
class CreateViewCliente(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear_cliente.html'
    success_url = reverse_lazy('home')
    login_url = '/' 

    def test_func(self):
        if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.proyecto:
            return False
        if self.request.user.is_superuser:
            return True
        return self.request.user.perfil.rol == 'Administrador'

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
    success_url = reverse_lazy('home')
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
        # Le pasamos el proyecto al formulario para que filtre los clientes
        kwargs['proyecto'] = self.request.user.perfil.proyecto
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        proyecto = self.request.user.perfil.proyecto
        
        if self.request.POST:
            data['detalles'] = DetallePedidoFormSet(
                self.request.POST, 
                form_kwargs={'proyecto': proyecto}
            )
        else:
            data['detalles'] = DetallePedidoFormSet(
                form_kwargs={'proyecto': proyecto}
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['detalles']
        
        if detalles.is_valid():
            with transaction.atomic():
                form.instance.proyecto = self.request.user.perfil.proyecto
                form.instance.vendedor = self.request.user
                self.object = form.save()
                
                detalles.instance = self.object
                detalles.save()
                
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))