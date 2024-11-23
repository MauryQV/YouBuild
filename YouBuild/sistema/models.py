from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta

# Departamento
class DepartamentoDB(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre del departamento")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre


# Provincia
class ProvinciaDB(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre de la provincia")
    departamento_fk = models.ForeignKey(DepartamentoDB, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"

    def __str__(self):
        return self.nombre


# Municipio
class MunicipioDB(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre del municipio")
    provincia_fk = models.ForeignKey(ProvinciaDB, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nombre


class UsuarioDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=50, verbose_name="Nombre completo", null=True)
    municipio_fk = models.ForeignKey('MunicipioDB', on_delete=models.CASCADE, null=True, blank=True)
    direccion_1 = models.CharField(max_length=255, verbose_name="Dirección", null=True)
    telefono = models.CharField(
        max_length=15, verbose_name="Número de celular",
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número debe estar en el formato: '+59199999999'. Hasta 15 dígitos.")]
    )
    imagen_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, default='perfil/perfil.png',verbose_name="Foto de perfil")
    qr_imagen = models.ImageField(upload_to='qr/', null=True, blank=True, verbose_name="Código QR")
    intentos_fallidos_password = models.IntegerField(default=0)
    bloqueo_password_hasta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return self.user.username
    
    def bloquear_cambio_password(self):
        self.intentos_fallidos_password = 0
        self.bloqueo_password_hasta = timezone.now() + timedelta(hours=24)
        self.save()

    def incrementar_intentos_fallidos(self):
        self.intentos_fallidos_password += 1
        if self.intentos_fallidos_password >= 5:
            self.bloquear_cambio_password()
        else:
            self.save()

    def restablecer_intentos(self):
        self.intentos_fallidos_password = 0
        self.bloqueo_password_hasta = None
        self.save()
    
    @property
    def esta_bloqueado(self):
        return self.bloqueo_password_hasta and timezone.now() < self.bloqueo_password_hasta


# Carrito
class CarritoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def agregar_producto(self, producto, cantidad=1):
        carrito_producto, created = CarritoProductoDB.objects.get_or_create(
            carrito_fk=self, producto_fk=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            carrito_producto.cantidad = F('cantidad') + cantidad
            carrito_producto.save()

    def eliminar_producto(self, producto):
        CarritoProductoDB.objects.filter(carrito_fk=self, producto_fk=producto).delete()

    def actualizar_cantidad(self, producto, cantidad):
        if cantidad <= 0:
            self.eliminar_producto(producto)
        else:
            carrito_producto = CarritoProductoDB.objects.filter(carrito_fk=self, producto_fk=producto).first()
            if carrito_producto:
                carrito_producto.cantidad = cantidad
                carrito_producto.save()

    def calcular_total(self):
        return self.carritoproductodb_set.aggregate(
            total=Sum(F('cantidad') * F('producto_fk__precio'))
        )['total'] or 0

    def __str__(self):
        return f"Carrito de {self.usuario_fk}"


class CategoriaDb(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la categoría")
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True, verbose_name="Imagen de la categoría")  # Campo de imagen

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre



# Subcategoria
class SubcategoriaDB(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la subcategoría")
    categoria_fk = models.ForeignKey(CategoriaDb, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return self.nombre


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models

class ProductoDb(models.Model): 
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('promocion', 'En Promoción'),
        ('vendido', 'Vendido'),
    ]
    
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    detalle = models.TextField(max_length=500, verbose_name="Detalle")
    precio = models.FloatField(verbose_name="Precio", validators=[MinValueValidator(0.0), MaxValueValidator(99999.9)])
    descuento = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name="Descuento (%)")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado del Producto")
    fecha_inicio_promocion = models.DateTimeField(null=True, blank=True, verbose_name="Inicio de Promoción")
    fecha_fin_promocion = models.DateTimeField(null=True, blank=True, verbose_name="Fin de Promoción")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para la venta")  # Para activar o desactivar el producto manualmente
    categoria_fk = models.ForeignKey(CategoriaDb, on_delete=models.CASCADE, null=True, blank=True)
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    municipio_fk = models.ForeignKey(MunicipioDB, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipio")
    direccion_1 = models.CharField(max_length=255, verbose_name="Dirección 1", null=True, blank=True)
    visitas = models.PositiveIntegerField(default=0, verbose_name="Visitas")
    cantidad = models.IntegerField(default=1)
    activo = models.BooleanField(default=True, verbose_name="Activo")  # Campo para soft delete.

    class Meta:
        db_table = "productos"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validación para asegurar que la fecha de fin sea posterior a la fecha de inicio
        if self.fecha_inicio_promocion and self.fecha_fin_promocion:
            if self.fecha_fin_promocion <= self.fecha_inicio_promocion:
                raise ValidationError("La fecha de fin de promoción debe ser posterior a la fecha de inicio.")

    def precio_final(self):
        """
        Calcula el precio final aplicando el descuento si el producto está en promoción.
        """
        if self.esta_en_promocion():
            return self.precio * (1 - self.descuento / 100)
        return self.precio

    def esta_en_promocion(self):
        """
        Verifica si el producto está actualmente en promoción.
        """
        if self.estado == 'promocion':
            # Comprueba si la fecha actual está dentro del rango de promoción
            ahora = timezone.now()
            if self.fecha_inicio_promocion and self.fecha_fin_promocion:
                return ahora <= self.fecha_fin_promocion
        return False

    def dias_restantes_promocion(self):
       
        ahora = timezone.now()
        if self.esta_en_promocion() and self.fecha_fin_promocion:
            delta = self.fecha_fin_promocion - ahora
            return delta.days
        return 0
    
    def tiempo_restante_promocion(self):
        ahora = timezone.now()
        if self.esta_en_promocion() and self.fecha_fin_promocion:
           delta = self.fecha_fin_promocion - ahora
           return int(delta.total_seconds())
        return 0
    
    def ajustar_stock(self, cantidad, operacion='restar'):
        if operacion == 'restar':
            if self.cantidad < cantidad:
                raise ValueError("Stock insuficiente para realizar esta operación.")
            self.cantidad -= cantidad
        elif operacion == 'sumar':
            self.cantidad += cantidad
        self.save()


# ImagenProducto
class ImagenProductoDB(models.Model):
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos", null=True)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return self.producto_fk.nombre

# TipoPago
class TipoPagoDB(models.Model):
    nombre = models.CharField(max_length=30, verbose_name="Nombre_tipo_de_pago")

    class Meta:
        db_table = "tipo_de_pago"
        verbose_name = "TipoPago"

    def __str__(self):
        return self.nombre


class PagoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE, null=True, blank=True)
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Producto Comprado")
    tipo_pago_fk = models.ForeignKey(TipoPagoDB, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(verbose_name="Fecha de pago", null=False, blank=False, db_index=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")

    class Meta:
        db_table = "pago"
        verbose_name_plural = "pagos"

    def save(self, *args, **kwargs):
        # Al guardar el pago, marca el producto como 'vendido'
        if self.producto_fk:
            self.producto_fk.estado = 'vendido'
            self.producto_fk.save()
        super().save(*args, **kwargs)


# CarritoProducto
class CarritoProductoDB(models.Model):
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE)
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def calcular_subtotal(self):
        return self.cantidad * self.producto_fk.precio_final()

    def __str__(self):
        return f"{self.producto_fk.nombre} (x{self.cantidad}) en el carrito"


# Carrusel
class CarruselDB(models.Model):
    imagen = models.ImageField(upload_to="carrusel", null=True)

    class Meta:
        verbose_name = "Carrusel"
        verbose_name_plural = "Carruseles"
        
class ListaFavoritosDB(models.Model):
    usuario = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, related_name="wishlist")
    producto = models.ForeignKey(ProductoDb, on_delete=models.CASCADE, related_name="favoritos")
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f"{self.usuario.user} - {self.producto.nombre}"

    def agregar_producto(self, producto):
        _, created = ListaFavoritosDB.objects.get_or_create(
            usuario=self.usuario, 
            producto=producto
        )
        return created  # Retorna True si fue creado, False si ya existía

    def eliminar_producto(self, producto):
        ListaFavoritosDB.objects.filter(usuario=self.usuario, producto=producto).delete()

    def contar_productos(self):
        return ListaFavoritosDB.objects.filter(usuario=self.usuario).count()
    
class Transaccion(models.Model):
    COMPRA = 'Compra'
    VENTA = 'Venta'
    TIPO_CHOICES = [
        (COMPRA, 'Compra'),
        (VENTA, 'Venta'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(ProductoDb, on_delete=models.CASCADE, related_name="transacciones")
    cantidad = models.PositiveIntegerField()
    detalles = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def calcular_precio_total(self):
        return self.cantidad * self.producto.precio_final()

    @property
    def precio_total(self):
        return self.calcular_precio_total()

    def clean(self):
        if self.tipo == self.COMPRA and self.producto.cantidad < self.cantidad:
            raise ValidationError("El producto no tiene suficiente stock disponible.")

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
