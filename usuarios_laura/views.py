from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DeleteView,
    DetailView
)
from .models import *
from usuarios_laura.formularios.usuario_forms import UsuarioForm



def home(request):
    contexto = {
        'mensaje': 'Bienvenido a usuarios',
        "user": request.user
    }
    return render(request, 'index.html', contexto)


################# CRUD USUARIO #################
class CreateViewUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Usuario/crear_usuario.html'
    success_url = '/home/'