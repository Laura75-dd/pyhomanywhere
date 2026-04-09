from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from proveedores.views import home
from .views import *


urlpatterns = [

    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('', LogoutView.as_view(next_page='login'), name='logout'), # logout para que puedan cerrar sesión y los mande al login de nuevo
    
    #path('home/',home, name='home'),

    #URLS CRUD CLIENTE
    path('clientes/crear/', CreateViewCliente.as_view(), name='crear_cliente'),

    # URLS CRUD PEDIDO (TICKET)
    path('pedidos/crear/', CreateViewPedido.as_view(), name='crear_pedido'),

    # URL PARA CAMBIAR EL ESTADO DEL PEDIDO
    path('pedidos/estado/<int:pedido_id>/<str:nuevo_estado>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
]