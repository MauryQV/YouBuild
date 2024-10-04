from django.contrib import admin
from .models import *

# Define la clase ImagenProductoInline primero
class ImagenProductoInline(admin.TabularInline):
    model = ImagenProductoDb
    extra = 2  # Número de imágenes adicionales que se pueden agregar en el admin

# Ahora registra el modelo ProductoDb con la inline
@admin.register(ProductoDb)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]

# El resto de los modelos registrados
@admin.register(CategoriaDb)
class CategoriaAdmin(admin.ModelAdmin):
    fields = ["nombre"]
    list_display = ["nombre"]

@admin.register(DepartamentoDB)
class DepartamentoAdmin(admin.ModelAdmin):
    fields = ["nombre"]
    list_display = ["nombre"]

@admin.register(ProvinciaDB)
class ProvinciaAdmin(admin.ModelAdmin):
     fields = ["nombre","departamento_fk"]
     list_display = ["nombre"]

@admin.register(MunicipioDB)
class MunicipioAdmin(admin.ModelAdmin):
     fields = ["nombre","provincia_fk"]
     list_display = ["nombre"]

admin.site.register(UsuarioDB)
admin.site.register(CarritoDB)
admin.site.register(TipoPagoDB)    
admin.site.register(PagoDB)
admin.site.register(CarritoProductoDB)
admin.site.register(CarruselDB)

# Finalmente, registra el modelo de imagen también
admin.site.register(ImagenProductoDb)
