from django.shortcuts import render, get_object_or_404
from .models import ProductoDb, CategoriaDb, CarruselDB

# Vista principal



def IndexView(request): 
    productos = ProductoDb.objects.all().order_by("id")  
    carruseles = CarruselDB.objects.all().order_by("id")
    return render(request, "index.html", {"producto": productos, "carrusel": carruseles})

def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    return render(request, "detalle_producto.html", {"producto": producto})
