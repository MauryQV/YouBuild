from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, F

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
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def agregar_producto(self, producto, cantidad=1):
        """Agrega un producto al carrito o actualiza su cantidad si ya está en el carrito."""
        carrito_producto, created = CarritoProductoDB.objects.get_or_create(
            carrito_fk=self, producto_fk=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            carrito_producto.cantidad = F('cantidad') + cantidad  # Usamos F() para evitar una lectura adicional
            carrito_producto.save()

    def eliminar_producto(self, producto):
        """Elimina un producto del carrito."""
        CarritoProductoDB.objects.filter(carrito_fk=self, producto_fk=producto).delete()

    def actualizar_cantidad(self, producto, cantidad):
        """Actualiza la cantidad de un producto en el carrito o lo elimina si la cantidad es 0."""
        if cantidad <= 0:
            self.eliminar_producto(producto)
        else:
            carrito_producto = CarritoProductoDB.objects.filter(carrito_fk=self, producto_fk=producto).first()
            if carrito_producto:
                carrito_producto.cantidad = cantidad
                carrito_producto.save()

    def calcular_total(self):
        """Calcula el total del carrito sumando los subtotales de cada producto."""
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
    fecha = models.DateField(verbose_name="Fecha_de_pago", null=False, blank=False, db_index=True)  # Índice en fecha
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    
    class Meta:
        db_table = "pago"  
        verbose_name_plural = "pagos"
    
    
class CarritoProductoDB(models.Model):
    carrito_fk = models.ForeignKey(CarritoDB, on_delete=models.CASCADE)
    producto_fk = models.ForeignKey(ProductoDb, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def calcular_subtotal(self):
        return self.cantidad * self.producto_fk.precio

    def __str__(self):
        return f"{self.producto_fk.nombre} (x{self.cantidad}) en el carrito"
        
class CarruselDB(models.Model):
    imagen = models.ImageField(upload_to="carrusel",null=True)
    
    class Meta:
         verbose_name = "Carrusel"
         verbose_name_plural = "Carruseles"
        


    
