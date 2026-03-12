from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from proveedores.views import home
from .views import *


urlpatterns = [

    path('', LoginView.as_view(template_name='login.html'), name='login'),
    
    path('home/',home, name='home'),

    #URLS CRUD CLIENTE
    path('clientes/crear/', CreateViewCliente.as_view(), name='crear_cliente'),

    # URLS CRUD PEDIDO (TICKET)
    path('pedidos/crear/', CreateViewPedido.as_view(), name='crear_pedido'),
]