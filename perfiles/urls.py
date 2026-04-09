from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('', LogoutView.as_view(next_page='login'), name='logout'), # logout para que puedan cerrar sesión y los mande al login de nuevo    

    #path('home/', home, name='home'),

    #URLS CRUD PERFIL
    path('perfiles/crear/', CreateViewPerfil.as_view(), name='crear_perfil'),

    #vista para datos los perfiles del equipo
    path('datos/perfil/', datos_perfil, name='datos_perfil'), 

    #vista para listar los perfiles del equipo
    path('equipo/', ListViewPerfil.as_view(), name='lista_equipo'),

    #vista para editar el perfil del usuario
    path('perfil/editar/', UpdateViewPerfil.as_view(), name='editar_perfil'),
    
]