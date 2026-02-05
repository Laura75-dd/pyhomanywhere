from django.urls import path
from .views import *

urlpatterns = [

    path('home/', home, name='home'),

    #URLS CRUD USUARIOS
    path('usuarios/crear/', CreateViewUsuario.as_view(), name='crear_usuario'),
    
]