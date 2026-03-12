from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.admin import UserAdmin 
from .models import Perfil

# 1. Agregamos el Perfil para que se pueda editar junto con el Usuario
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Información del Perfil'

# 2. Creamos nuestro Admin heredando de UserAdmin (Esto recupera la pantalla del profe)
class MiUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    
    # Opcional: Si quieres mantener las columnas de Rol y Puesto en la lista general
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

# 3. Desregistramos el User roto y lo registramos con la magia restaurada
admin.site.unregister(User)
admin.site.register(User, MiUserAdmin)

# Registramos el perfil de forma individual por si quieres verlo por separado
admin.site.register(Perfil)