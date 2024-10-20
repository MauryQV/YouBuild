from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Departamento
class DepartamentoDB(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre del departamento")  # Convención de nombres
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"  # Cambio de mayúscula para consistencia

    def __str__(self):
        return self.nombre


# Provincia
class ProvinciaDB(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Nombre de la provincia")
    departamento_fk = models.ForeignKey(DepartamentoDB, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"  # Cambio a mayúscula para consistencia

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
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    municipio_fk = models.ForeignKey('MunicipioDB', on_delete=models.CASCADE, null=True, blank=True)  # Campo Municipio
    direccion = models.CharField(max_length=255, null=True, blank=True)
    imagen_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)  # Campo Imagen de Perfil

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return self.user.username


# Carrito
class CarritoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Añadir un campo de fecha de creación
    
    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def calcular_total(self):
        total = sum([item.calcular_subtotal() for item in self.carritoproductodb_set.all()])
        return total

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


# Producto
class ProductoDb(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    detalle = models.TextField(max_length=200, verbose_name="Detalle")
    precio = models.FloatField(verbose_name="Precio", validators=[MinValueValidator(0.0), MaxValueValidator(99999.9)])
    categoria_fk = models.ForeignKey(CategoriaDb, on_delete=models.CASCADE, null=True, blank=True)
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    visitas = models.PositiveIntegerField(default=0, verbose_name="Visitas")  # Nuevo campo para visitas
    cantidad = models.IntegerField(default=1)

    class Meta:
        db_table = "productos"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
      
class ImagenProductoDB(models.Model):
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos", null=True)
    
    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"
        
    def __str__(self):
        return self.producto_fk.nombre
    
class TipoPagoDB(models.Model):  
    nombre = models.CharField(max_length=30,verbose_name="Nombre_tipo_de_pago")
    class Meta:
        db_table = "tipo_de_pago"  # Convención de nombres en minúsculas para tablas
        verbose_name = "TipoPago"
    def __str__(self):
        return self.nombre
    
class PagoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB,on_delete=models.CASCADE,null=True, blank=True)
    carrito_fk = models.ForeignKey(CarritoDB,on_delete=models.CASCADE,null=True,blank=True)
    tipo_pago_fk = models.ForeignKey(TipoPagoDB,on_delete=models.CASCADE,null=True,blank=True)
    fecha = models.DateField(verbose_name="Fecha_de_pago",null=False, blank=False)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    
    class Meta:
        db_table = "pago"  
        verbose_name_plural = "pagos"
    
    
class CarritoProductoDB(models.Model):
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE)
    producto_fk = models.ForeignKey('ProductoDB', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Carrito Producto"
        verbose_name_plural = "Carrito Productos"
        unique_together = ('carrito_fk', 'producto_fk')  # Evitar productos duplicados en el mismo carrito

    def calcular_subtotal(self):
        return self.producto_fk.precio * self.cantidad

    def __str__(self):
        return f"{self.producto_fk.nombre} (x{self.cantidad}) en el carrito de {self.carrito_fk.usuario_fk}"
        
        
class CarruselDB(models.Model):
    imagen = models.ImageField(upload_to="carrusel",null=True)
    
    class Meta:
         verbose_name = "Carrusel"
         verbose_name_plural = "Carruseles"
        


    
