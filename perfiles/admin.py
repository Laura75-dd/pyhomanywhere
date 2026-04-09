from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.admin import UserAdmin 
from .models import Perfil

# 1. Agrega el Perfil para que se pueda editar junto con el Usuario
# class PerfilInline(admin.StackedInline):
#     model = Perfil
#     can_delete = False
#     verbose_name_plural = 'Información del Perfil'

# 2. Crea el Admin heredando de UserAdmin
class MiUserAdmin(UserAdmin):
    #inlines = (PerfilInline,)
    
    # Op: mantener las columnas de Rol y Puesto en la lista general
    list_display = ('username', 'email', 'get_rol', 'get_puesto', 'is_staff')

    def get_rol(self, instance):
        if hasattr(instance, 'perfil') and instance.perfil.rol:
            return instance.perfil.rol
        return '-'
    get_rol.short_description = 'ROL'

    def get_puesto(self, instance):
        if hasattr(instance, 'perfil') and instance.perfil.puesto:
            return instance.perfil.puesto
        return '-'
    get_puesto.short_description = 'PUESTO'

# 3. Desregistra el User roto y lo registra con el nuevo admin que incluye el Perfil
admin.site.unregister(User)
admin.site.register(User, MiUserAdmin)

# Registra el perfil de forma individual para ver por separado
admin.site.register(Perfil)