from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Sum, F

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
        max_length=15, verbose_name="Número de teléfono",
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número debe estar en el formato: '+59199999999'. Hasta 15 dígitos.")]
    )
    imagen_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, default='perfil/perfil.png',verbose_name="foto de perfil")
    qr_imagen = models.ImageField(upload_to='qr/', null=True, blank=True, verbose_name="Código QR")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return self.user.username


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


# Categoria
class CategoriaDb(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

#Subcategoria    
class SubcategoriaDB(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la subcategoría")
    categoria_fk = models.ForeignKey(CategoriaDb, on_delete=models.CASCADE, related_name="subcategorias")

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

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


class ProductoDb(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    detalle = models.TextField(max_length=200, verbose_name="Detalle")
    precio = models.FloatField(verbose_name="Precio", validators=[MinValueValidator(0.0), MaxValueValidator(99999.9)])
    categoria_fk = models.ForeignKey(CategoriaDb, on_delete=models.CASCADE, null=True, blank=True)
    subcategoria_fk = models.ForeignKey(SubcategoriaDB, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Subcategoría")  # Nuevo campo
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    municipio_fk = models.ForeignKey(MunicipioDB, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipio")
    direccion_1 = models.CharField(max_length=255, verbose_name="Dirección 1", null=True, blank=True)
    visitas = models.PositiveIntegerField(default=0, verbose_name="Visitas")
    cantidad = models.IntegerField(default=1)
    municipio_fk = models.ForeignKey('MunicipioDB', on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True)  # Permitir nulos

    class Meta:
        db_table = "productos"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre




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


# Pago
class PagoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE, null=True, blank=True)
    tipo_pago_fk = models.ForeignKey(TipoPagoDB, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(verbose_name="Fecha_de_pago", null=False, blank=False, db_index=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")

    class Meta:
        db_table = "pago"
        verbose_name_plural = "pagos"


# CarritoProducto
class CarritoProductoDB(models.Model):
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE)
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def calcular_subtotal(self):
        return self.cantidad * self.producto_fk.precio

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
        """ Agregar un producto a la lista de deseos """
        _, created = ListaFavoritosDB.objects.get_or_create(
            usuario=self.usuario, 
            producto=producto
        )
        return created  # Retorna True si fue creado, False si ya existía

    def eliminar_producto(self, producto):
        """ Eliminar un producto de la lista de deseos """
        ListaFavoritosDB.objects.filter(usuario=self.usuario, producto=producto).delete()

    def contar_productos(self):
        """ Contar la cantidad de productos en la lista de deseos """
        return ListaFavoritosDB.objects.filter(usuario=self.usuario).count()