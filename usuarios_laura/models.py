from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  #
    rol = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('empleado', 'Empleado'),
            ('proveedor', 'Proveedor'),
        ]
    )

    def __str__(self):
        return self.nombre
