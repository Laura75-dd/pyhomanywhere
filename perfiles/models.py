from django.db import models
from django.contrib.auth.models import User

# =========================================================
# MODELO PERFIL: Extiende los datos del usuario de Django
# =========================================================
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    
    PUESTOS = [
        ('Chef / Cocinero', 'Chef / Cocinero'),
        ('Cajero', 'Cajero'),
        ('Mesero', 'Mesero'),
        ('Barista', 'Barista'),
        ('Otro', 'Otro'),
    ]

    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    rol = models.CharField(max_length=20, choices=ROLES, default='Empleado', verbose_name="Rol")
    puesto = models.CharField(max_length=50, choices=PUESTOS, blank=True, null=True, verbose_name="Puesto")
    puesto_personalizado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Puesto Específico")
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)    
    
    # Conecta al empleado o administrador con su lugar de trabajo.
    proyecto = models.ForeignKey(
        'proyectos.Proyecto', 
        on_delete=models.CASCADE, 
        null=True, # Puede ser nulo porque (El Superusuario) no tiene proyecto asignado
        blank=True, 
        related_name='miembros',
        verbose_name="Proyecto Asignado"
    )

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.rol}"

    # Facilitan preguntar en el código qué rol tiene el usuario
    @property
    def is_administrador(self):
        return self.rol == 'Administrador'

    @property
    def is_empleado(self):
        return self.rol == 'Empleado'

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"