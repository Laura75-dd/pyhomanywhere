from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# =========================================================
# MODELO PROYECTO: Representa a cada negocio que usa tu app
# =========================================================
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej. Taquería Los Compadres")
    descripcion = models.TextField(blank=True, null=True)
    dias_de_venta = models.CharField(max_length=100, help_text="Ej. Fines de semana", blank=True, null=True) 
    
    # Define quién es el dueño del negocio. Si el usuario se borra, se borra el negocio también.
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'perfil__rol': 'Administrador'}, 
        related_name='proyectos_administrados' 
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Permite "apagar" un negocio sin borrar sus datos (ej. vacasiones o cierran temporalmente)
    esta_activo = models.BooleanField(default=True, help_text="Desmarcar si el negocio cierra temporalmente")

    def __str__(self):
        # Muestra el nombre del negocio y su dueño en el panel de administración
        return f"{self.nombre} (Dueño: {self.administrador.username})"


# =========================================================
# MODELO PRODUCTO: Los artículos que el negocio vende (Menú)
# =========================================================
class Producto(models.Model):
    # Relaciona el producto con un negocio específico. Si se borra el negocio, se borran sus productos.
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='productos')
    
    nombre = models.CharField(max_length=100, help_text="Ej. Pizza de Pepperoni") 
    variante = models.CharField(max_length=50, blank=True, null=True, help_text="Ej. Familiar, Individual") 
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # Permite ocultar un producto del menú si hoy no hay ingredientes para prepararlo
    disponible = models.BooleanField(default=True)

    def clean(self):
        # FUNCIÓN DE VALIDACIÓN: Revisa los datos ANTES de guardarlos.
        # Evita que un empleado registre un precio negativo por error.
        if self.precio is not None and self.precio < 0:
            raise ValidationError("El precio no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        # Formatea cómo se ve el producto en listas. Ej: "Pizza (Familiar) - $150.00 [Agotado]"
        variante_str = f" ({self.variante})" if self.variante else ""
        estado = "" if self.disponible else " [Agotado]"
        return f"{self.nombre}{variante_str} - ${self.precio}{estado}"


# =========================================================
# MODELO INVENTARIO: Control de insumos para preparar productos
# =========================================================
class Inventario(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='inventario')
    
    insumo = models.CharField(max_length=100, help_text="Ej. Cajas de Pizza, Harina, Queso")
    cantidad_actual = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20, help_text="Ej. Kg, Litros, Piezas")
    
    # La cantidad límite en la que el sistema debe lanzar una advertencia
    stock_minimo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="El sistema avisará cuando la cantidad actual baje de este número"
    )

    @property
    def alerta_stock(self):
        # Devuelve 'True' (Verdadero) si la cantidad actual es menor o igual al stock mínimo.
        # Sirve para pintar la fila de rojo en las tablas HTML.
        return self.cantidad_actual <= self.stock_minimo

    def __str__(self):
        return f"{self.insumo}: {self.cantidad_actual} {self.unidad_medida} (Min: {self.stock_minimo})"