from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

# =========================================================
# MODELO CLIENTE: Directorio de clientes de cada negocio
# =========================================================
class Cliente(models.Model):
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, related_name='clientes')
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    Pedidos = models.ManyToManyField('Pedido', blank=True, related_name='clientes_pedidos')
    def __str__(self):
        return f"{self.nombre} (Cliente de {self.proyecto.nombre})"


# =========================================================
# MODELO PEDIDO: Representa una "Orden de Compra" o "Ticket"
# =========================================================
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente 🔴'),
        ('ATENDIENDO', 'Atendiendo 🟡'),
        ('LIBERADO', 'Liberado 🟢'),
        ('CANCELADO', 'Cancelado ⚫'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')

    # 1. es opcional, no borra el pedido si se elimina al cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    # 2. Para el nombre rápido cuando no se quieren registrar
    nombre_invitado = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombre (Cliente de paso)")
    
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.CASCADE, related_name='pedidos_negocio')
    fecha = models.DateTimeField(auto_now_add=True) 

  
    # El cajero o mesero que atendió este pedido
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Si el vendedor renuncia, el ticket de venta se conserva
        related_name='pedidos_realizados',
        null=True, blank=True
    )

    def clean(self):
        # 1. El cliente debe ser cliente del mismo negocio donde se hace el pedido.
        if self.cliente and self.proyecto:
            if self.cliente.proyecto != self.proyecto:
                raise ValidationError("Error: El cliente seleccionado pertenece a otro negocio.")
        
        # 2. El vendedor debe ser empleado de este negocio (no de otro).
        if self.vendedor and hasattr(self.vendedor, 'perfil'):
            if self.vendedor.perfil.proyecto != self.proyecto:
                raise ValidationError("Error: El vendedor no está asignado a este negocio.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total(self):
        # Obtiene todos los productos dentro de este pedido y suma sus subtotales.
        # Da como resultado el monto final a cobrarle al cliente.
        detalles = self.detalles.all()
        return sum(detalle.subtotal for detalle in detalles)
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"
    
    def __str__(self):
        # 3.  Muestra el nombre registrado, o el nombre de invitado
        nombre_mostrar = self.cliente.nombre if self.cliente else (self.nombre_invitado or "Sin nombre")
        return f"Pedido #{self.id} - {nombre_mostrar} ({self.estado})"


# # =========================================================
# # MODELO DETALLE PEDIDO: Los productos específicos dentro del Ticket
# # =========================================================
class DetallePedido(models.Model):
    # Conecta este detalle con su pedido (Ticket)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    
    # Conecta con el catálogo de productos. 
    # on_delete=RESTRICT evita que se borre del menú por ejemplo una "Pizza" si ya se vendió alguna vez.
    producto = models.ForeignKey('proyectos.Producto', on_delete=models.RESTRICT) 
    cantidad = models.PositiveIntegerField() 

    def clean(self):
        # CANDADO DE SEGURIDAD:
        # Evita que se venda un producto que pertenece a otro restaurante.
        if self.pedido and self.producto:
            if self.pedido.proyecto != self.producto.proyecto:
                raise ValidationError("Error: Estás intentando vender un producto de otro negocio.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        # Calcula el costo de esta línea del ticket (ej. 3 x Pizza de $100 = $300)
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal}"