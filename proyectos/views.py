from django.shortcuts import render, redirect
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
from proyectos.formularios.proyecto_forms import ProyectoForm, ProductoForm, InventarioForm
from clientes.models import *
from proveedores.models import Proveedor

# ==========================================
# VISTA PRINCIPAL (DASHBOARD DEL NEGOCIO)
# ==========================================

@login_required(login_url='/')
def home(request):
    if not hasattr(request.user, 'perfil') or not request.user.perfil.proyecto:
        return render(request, 'error_deregistro.html')

    proyecto_actual = request.user.perfil.proyecto

    # 2. HACEMOS TODOS LOS CÁLCULOS AQUÍ MISMO
    total_clientes = Cliente.objects.filter(proyecto=proyecto_actual).count()
    total_pedidos = Pedido.objects.filter(proyecto=proyecto_actual).count()
   
   # Excluye tanto los cancelados como los liberados de los contadores
    pedidos_activos = Pedido.objects.filter(proyecto=proyecto_actual).exclude(estado__in=['CANCELADO', 'LIBERADO']).count()
    # Excluye los mismos estados de la lista que se pinta en las tarjetas
    lista_pedidos = Pedido.objects.filter(proyecto=proyecto_actual).exclude(estado__in=['CANCELADO', 'LIBERADO']).order_by('-fecha')

    context = {
        'mensaje': f'Gestión Principal - {proyecto_actual.nombre}',
        'user': request.user,
        'perfil': request.user.perfil,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'pedidos_activos': pedidos_activos,
        'lista_pedidos_activos': lista_pedidos,
    }
    
    return render(request, 'index.html', context)

# ==========================================
# CRUD PROYECTO (CREACIÓN DEL NEGOCIO)
# ==========================================
# 1. CREAR (SuperUser o Admin sin proyecto asignado)
class CreateViewProyecto(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'Proyecto/crear_proyecto.html'
    success_url = '/home/' 
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
    success_url = '/home/'
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
    

# ==========================================
# CRUD PRODUCTO (ARTÍCULOS DEL MENÚ)
# ==========================================

class CreateViewProducto(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Proyecto/crear_producto.html'
    success_url = '/home/'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        return perfil and perfil.rol in ['Administrador'] and perfil.proyecto is not None
    
    def form_valid(self, form):
        nuevo_producto = form.save(commit=False)
        perfil = self.request.user.perfil
        nuevo_producto.proyecto = perfil.proyecto
        nuevo_producto.save()
        return super().form_valid(form)
    
class UpdateViewProducto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Proyecto/editar_producto.html' 
    success_url = '/home/'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        producto_a_editar = self.get_object()
        
        # Valida si es Administrador y si el producto pertenece a SU proyecto
        return perfil and perfil.rol in ['Administrador'] and producto_a_editar.proyecto == perfil.proyecto
    
class DetailViewProducto(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Producto
    template_name = 'Proyecto/detalle_producto.html'
    context_object_name = 'producto'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        producto_a_ver = self.get_object()
        
        # Valida que el producto que intenta ver pertenezca al proyecto del usuario
        return perfil and producto_a_ver.proyecto == perfil.proyecto
    
class ListViewProducto(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'Proyecto/lista_productos.html'
    context_object_name = 'productos'
    login_url = '/'

    def get_queryset(self):
        # Aseguramos que el usuario solo vea los productos de su proyecto actual
        perfil = getattr(self.request.user, 'perfil', None)
        if perfil and perfil.proyecto:
            return Producto.objects.filter(proyecto=perfil.proyecto)
        return Producto.objects.none()

# ==========================================================
# CRUD INVENTARIO (INSUMOS PARA PREPARAR LOS PRODUCTOS)
# ==========================================================

class CreateViewInventario(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'Proyecto/crear_inventario.html'
    success_url = '/home/'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        return perfil and perfil.rol == 'Administrador'
    
    def form_valid(self, form):
        nuevo_inventario = form.save(commit=False)
        perfil = self.request.user.perfil
        nuevo_inventario.proyecto = perfil.proyecto
        nuevo_inventario.save()
        return super().form_valid(form)

class UpdateViewInventario(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'Proyecto/editar_inventario.html' 
    success_url = '/home/'
    login_url = '/'


    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        inventario_a_editar = self.get_object()
        
        # Valida si es Administrador y si el inventario pertenece a SU proyecto
        return perfil and perfil.rol == 'Administrador' and inventario_a_editar.proyecto == perfil.proyecto
    
class DetailViewInventario(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Inventario
    template_name = 'Proyecto/detalle_inventario.html'
    context_object_name = 'inventario'
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        perfil = getattr(self.request.user, 'perfil', None)
        inventario_a_ver = self.get_object()
        
        # Valida que el inventario que intenta ver pertenezca al proyecto del usuario
        return perfil and inventario_a_ver.proyecto == perfil.proyecto

class ListViewInventario(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'Proyecto/lista_inventario.html' 
    # 1. CAMBIO: Usamos plural para que coincida con tu HTML
    context_object_name = 'inventarios' 
    login_url = '/'

    def get_queryset(self):
        user = self.request.user
        
        # 2. JERARQUÍA: Si es Superusuario, ve absolutamente TODO el inventario del sistema
        if user.is_superuser:
            return Inventario.objects.all()

        # 3. JERARQUÍA: Si es Admin o Empleado, filtramos por su proyecto
        perfil = getattr(user, 'perfil', None)
        if perfil and perfil.proyecto:
            return Inventario.objects.filter(proyecto=perfil.proyecto)
        
        # Si no tiene proyecto asignado, no ve nada
        return Inventario.objects.none()