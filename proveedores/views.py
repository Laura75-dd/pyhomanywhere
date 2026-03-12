from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

# IMPORTACIONES DE SEGURIDAD
# LOGINREQUIREDMIXIN:
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import *
from proveedores.formularios.proveedor_forms import ProveedorForm, CompraInsumoForm

# ==========================================
# DASHBOARD DE PROVEEDORES
# ==========================================
@login_required(login_url='/')
def home(request):
    # Valida que el usuario tenga perfil y negocio
    if not hasattr(request.user, 'perfil') or not request.user.perfil.proyecto:
        return render(request, 'error_sin_negocio.html')

    contexto = {
        'mensaje': f'Proveedores de {request.user.perfil.proyecto.nombre}',
        "user": request.user
    }
    return render(request, 'index.html', contexto)

# ==========================================
# CRUD PROVEEDOR
# ==========================================
class CreateViewProveedor(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'Proveedor/crear_proveedor.html'
    success_url = reverse_lazy('home')
    login_url = '/'

    def form_valid(self, form):
        nuevo_proveedor = form.save(commit=False)
        # Amarra el proveedor al proyecto del usuario accedie por el perfil
        nuevo_proveedor.proyecto = self.request.user.perfil.proyecto
        nuevo_proveedor.save()
        return super().form_valid(form)

class ListViewProveedor(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'Proveedor/lista_proveedores.html'
    context_object_name = 'proveedores'
    login_url = '/'

    def get_queryset(self):
        # Filtro de solo ver proveedores de MI negocio
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.proyecto:
            return Proveedor.objects.filter(proyecto=self.request.user.perfil.proyecto)
        return Proveedor.objects.none() # Devuelve lista vacía si no tiene negocio

# ==========================================
# CRUD COMPRA INSUMO
# ==========================================
class CreateViewCompra(LoginRequiredMixin, CreateView):
    model = CompraInsumo
    form_class = CompraInsumoForm
    template_name = 'Proveedor/registrar_compra.html'
    success_url = reverse_lazy('home') 
    login_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Envia el proyecto del usuario actual al formulario
        if hasattr(self.request.user, 'perfil'):
            kwargs['proyecto'] = self.request.user.perfil.proyecto
        return kwargs

    def form_valid(self, form):
        nueva_compra = form.save(commit=False)
        # A. Amarra la compra al negocio actual
        nueva_compra.proyecto = self.request.user.perfil.proyecto
        # B. Registra QUIEN hizo la compra (El empleado logueado)
        nueva_compra.usuario_registro = self.request.user
        
        nueva_compra.save()
        return super().form_valid(form)