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
from proyectos.formularios.proyecto_forms import ProyectoForm

# ==========================================
# VISTA PRINCIPAL (DASHBOARD DEL NEGOCIO)
# ==========================================
@login_required(login_url='/')
def home(request):
    # Personaliza para el mensaje usando el Perfil del usuario
    perfil = getattr(request.user, 'perfil', None)
    
    if perfil and perfil.proyecto:
        nombre = perfil.proyecto.nombre
    else:
        nombre = "SmartDayz"
    
    stats = {
        'nuevos_clientes': 0,
        'total_pedidos': 0,
        'total_proveedores': 0,
    }
    
    contexto = {
        'mensaje': f'Bienvenido a la gestión operativa de {nombre}',
        'user': request.user,
        'perfil': perfil, # permite que el index.html sepa el rol
        'stats': stats,   # Para que no salgan vacías las tarjetas del inicio
    }
    return render(request, 'index.html', contexto) 


# ==========================================
# CRUD PROYECTO (CREACIÓN DEL NEGOCIO)
# ==========================================
# 1. CREAR (SuperUser o Admin sin proyecto asignado)
class CreateViewProyecto(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'Proyecto/crear_proyecto.html'
    success_url = reverse_lazy('home') 
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        perfil = getattr(self.request.user, 'perfil', None)
        return perfil and perfil.rol == 'Administrador'

    def form_valid(self, form):
        nuevo_proyecto = form.save(commit=False)
        nuevo_proyecto.administrador = self.request.user
        nuevo_proyecto.save()
        
        if not self.request.user.is_superuser:
            perfil = self.request.user.perfil
            perfil.proyecto = nuevo_proyecto
            perfil.save() 
        
        return super().form_valid(form)


# 2. EDITAR (Solo Administrador dueño del proyecto)
class UpdateViewProyecto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'Proyecto/editar_proyecto.html' 
    success_url = reverse_lazy('home')
    login_url = '/'

    def test_func(self):
        # El superusuario puede editar cualquier proyecto
        if self.request.user.is_superuser:
            return True
        
        # Obtenemos el perfil y el proyecto que se intenta editar
        perfil = getattr(self.request.user, 'perfil', None)
        proyecto_a_editar = self.get_object()
        
        # Valida si es Administrador y si es SU proyecto
        return perfil and perfil.rol == 'Administrador' and perfil.proyecto == proyecto_a_editar


# 3. Solo visualización para Empleados o Administradores de ese proyecto
class DetailViewProyecto(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Proyecto
    template_name = 'Proyecto/detalle_proyecto.html'
    context_object_name = 'proyecto'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        proyecto_a_ver = self.get_object()
        
        # Valida que el usuario pertenezca al proyecto que intenta ver
        return perfil and perfil.proyecto == proyecto_a_ver