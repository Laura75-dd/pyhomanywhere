from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('', LoginView.as_view(template_name='login.html'), name='login'),

    path('home/', home, name='home'),

    #URLS CRUD PERFIL
    path('perfiles/crear/', CreateViewPerfil.as_view(), name='crear_perfil'),
    
]