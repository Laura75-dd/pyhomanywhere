from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# =========================================================
# MODELO PROVEEDOR: El directorio de proveedores del negocio
# =========================================================
class Proveedor(models.Model):
    # Se usa la cadena 'proyectos.Proyecto' para que Django sepa a qué app y modelo apuntar 
    # sin causar un error de "importación circular".
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, related_name='proveedores')
    
    nombre = models.CharField(max_length=100, help_text="Ej. Frutería Don Juan")
    tipo = models.CharField(max_length=50, help_text="Ej. Frutas, Cajas, Refrescos")
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


# =========================================================
# MODELO COMPRA INSUMO: El registro de los gastos/compras
# =========================================================
class CompraInsumo(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras_realizadas')
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, related_name='gastos_insumos')

    # Registra qué empleado (o administrador) hizo la compra en el sistema
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Si el empleado es despedido, su registro de compra NO se borra
        null=True, 
        blank=True,
        help_text="Quién registró esta compra en el sistema"
    )

    fecha = models.DateTimeField(auto_now_add=True)
    nombre_insumo = models.CharField(max_length=100, help_text="Ej. Cajas de cartón, Manzanas")
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio por unidad")

    @property
    def total_a_pagar(self):
        # Calcula automáticamente cuánto costó la compra multiplicando cantidad por precio
        return self.cantidad * self.costo_unitario

    def clean(self):
        # CANDADO DE SEGURIDAD (Multitenancy): 
        # Verifica que el proveedor al que le estás comprando, pertenezca a tu mismo negocio.
        # Evita que el "Food Truck B" le asigne una compra a un proveedor de la "Cafetería A".
        if self.proveedor and self.proyecto:
            if self.proveedor.proyecto != self.proyecto:
                raise ValidationError("Error: Estás intentando registrar una compra con un proveedor de otro negocio.")

    def save(self, *args, **kwargs):
        # Fuerza a que el candado de seguridad (clean) se ejecute siempre que se guarde un registro
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_insumo} - Total: ${self.total_a_pagar} ({self.proveedor.nombre})"