from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

     path('', LoginView.as_view(template_name='login.html'), name='login'),
     path('', LogoutView.as_view(next_page='login'), name='logout'), # logout para que puedan cerrar sesión y los mande al login de nuevo

       # URL DASHBOARD
    path('home/', home, name='home'),


    #URLS CRUD PROYECTOS
    path('proyectos/crear/', CreateViewProyecto.as_view(), name='crear_proyecto'),
    # para editar y ver detalle, y para el ID del proyecto, por eso <int:pk>
    path('proyectos/editar/<int:pk>/', UpdateViewProyecto.as_view(), name='editar_proyecto'),
    path('proyectos/detalle/<int:pk>/', DetailViewProyecto.as_view(), name='detalle_proyecto'),

    #URLS CRUD PRODUCTOS
    path('productos/', ListViewProducto.as_view(), name='lista_productos'),
    path('productos/crear/', CreateViewProducto.as_view(), name='crear_producto'),
    path('productos/editar/<int:pk>/', UpdateViewProducto.as_view(), name='editar_producto'),
    path('productos/detalle/<int:pk>/', DetailViewProducto.as_view(), name='detalle_producto'),

    #URLS CRUD INVENTARIO
    path('inventario/lista/', ListViewInventario.as_view(), name='lista_inventario'),
    path('inventario/crear/', CreateViewInventario.as_view(), name='crear_inventario'),
    path('inventario/editar/<int:pk>/', UpdateViewInventario.as_view(), name='editar_inventario'),
    path('inventario/detalle/<int:pk>/', DetailViewInventario.as_view(), name='detalle_inventario'),

]
