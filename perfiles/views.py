from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from .models import Perfil
from .formularios.perfil_forms import PerfilForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from clientes.models import Cliente, Pedido
from proveedores.models import Proveedor

# ==========================================
# VISTA PRINCIPAL (DASHBOARD GENERAL)
# ==========================================
@login_required(login_url='/')
def home(request):
    # para evitar errores si entra el Admin (que no tiene perfil)
    perfil_usuario = getattr(request.user, 'perfil', None)

    if perfil_usuario and perfil_usuario.proyecto:
        nombre_negocio = perfil_usuario.proyecto.nombre

        # CUENTA LOS REGISTROS REALES EN LA BASE DE DATOS PARA ESTE NEGOCIO
        total_clientes = Cliente.objects.filter(proyecto=perfil_usuario.proyecto).count()
        total_pedidos = Pedido.objects.filter(proyecto=perfil_usuario.proyecto).count()
        total_proveedores = Proveedor.objects.filter(proyecto=perfil_usuario.proyecto).count()
    else:
        nombre_negocio = "SmartDayz Manager"
        total_clientes = 0
        total_pedidos = 0
        total_proveedores = 0

    contexto = {
        'mensaje': f'Bienvenido al panel de {nombre_negocio}',
        'perfil': perfil_usuario,
        'user': request.user,
        # MANDA LOS CONTADORES AL ARCHIVO HTML
        'stats': {
            'nuevos_clientes': total_clientes,
            'total_pedidos': total_pedidos,
            'total_proveedores': total_proveedores,
        }
    }
    return render(request, 'index.html', contexto)

# ==========================================
# CRUD PERFIL (GESTIÓN DEL EQUIPO)
# ==========================================

class CreateViewPerfil(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'perfil/registro_personal.html'
    success_url = reverse_lazy('home')
    login_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        perfil = getattr(self.request.user, 'perfil', None)
        return perfil and perfil.rol in ['Administrador', 'Empleado']

# ============================================================
# Este es el que se envia el usuario al formulario
# ============================================================
    def get_form_kwargs(self):
        kwargs = super(CreateViewPerfil, self).get_form_kwargs()
        # Aquí pone el usuario actual en los argumentos del formulario que tengo
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        admin_perfil = getattr(self.request.user, 'perfil', None)
        proyecto_a_asignar = admin_perfil.proyecto if admin_perfil else None

        # método save personalizado de mi PerfilForm
        form.save(proyecto_asignado=proyecto_a_asignar)

        return redirect(self.success_url)


class ListViewPerfil(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'perfiles/lista_equipo.html'
    context_object_name = 'empleados'
    login_url = '/'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Perfil.objects.all()

        perfil = getattr(self.request.user, 'perfil', None)

        if perfil and perfil.proyecto:
            return Perfil.objects.filter(proyecto=perfil.proyecto).exclude(usuario=self.request.user)

        return Perfil.objects.none()