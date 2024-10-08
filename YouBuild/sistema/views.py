from django.shortcuts import render, get_object_or_404
from .models import ProductoDb, CategoriaDb, CarruselDB

# Vista principal

def IndexView(request): 
    productos = ProductoDb.objects.all().order_by("id")  
    carruseles = CarruselDB.objects.all().order_by("id")
    return render(request, "index.html", {"producto": productos, "carrusel": carruseles})

def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    imagenes = producto.imagenes.all()
    return render(request, "detalle_producto.html", {"producto": producto,})

def BuscarView(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(nombre__icontains=q)
    print('Estos son los productos:')
    for producto in productos:
        print(producto)
    return render(request, 'index.html', {'producto': productos})

def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    producto.visitas += 1  
    producto.save()  
    return render(request, "detalle_producto.html", {"producto": producto})
