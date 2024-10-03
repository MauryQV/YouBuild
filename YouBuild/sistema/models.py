from django.db import models
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


# Usuario
class UsuarioDB(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre") 
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    contraseña = models.CharField(max_length=20, verbose_name="Contraseña")
    municipio_fk = models.ForeignKey(MunicipioDB, on_delete=models.CASCADE, null=True, blank=True)
    fecha_nac = models.DateField(verbose_name="Fecha_de_nacimiento",null=False, blank=False)
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# Carrito
class CarritoDB(models.Model):
    usuario_fk = models.ForeignKey(UsuarioDB, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"


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
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    class Meta:
        db_table = "productos"  # Convención de nombres en minúsculas para tablas
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

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
    producto_fk = models.ForeignKey('ProductoDb', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Carrito Producto"
        verbose_name_plural = "Carrito Productos"

    
