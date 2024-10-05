from django.contrib import admin
from .models import *
# Register your models here.
class ImagenInline(admin.TabularInline):
    model = ImagenProductoDB
    extra = 1

@admin.register(ProductoDb)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenInline]

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
    


    

    
    

