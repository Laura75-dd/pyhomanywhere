
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #URL DE MI APP USUARIOS
    path('',include('usuarios_laura.urls')),

    #URL DE MI APP PROYECTOS
    path('',include('proyectos_lau.urls')),

    #URL DE MI APP PROVEEDORES
    path('',include('proveedores_lau.urls')),

    #URL DE MI APP CLIENTES
    path('',include('clientes_lau.urls')),

]
