from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from proveedores.views import home
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # logout para que puedan cerrar sesión y los mande al login de nuevo  



    #URL DE MI APP PERFILES
    path('',include('perfiles.urls')),

    #URL DE MI APP PROYECTOS
    path('',include('proyectos.urls')),

    #URL DE MI APP PROVEEDORES
    path('',include('proveedores.urls')),

    #URL DE MI APP CLIENTES
    path('',include('clientes.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
