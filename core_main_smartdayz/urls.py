
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #URL DE MI APP PERFILES
    path('',include('perfiles.urls')),

    #URL DE MI APP PROYECTOS
    path('',include('proyectos.urls')),

    #URL DE MI APP PROVEEDORES
    path('',include('proveedores.urls')),

    #URL DE MI APP CLIENTES
    path('',include('clientes.urls')),

]
