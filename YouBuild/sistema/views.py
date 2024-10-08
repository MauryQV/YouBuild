from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductoDb, CategoriaDb, CarruselDB, CarritoDB, CarritoProductoDB

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
    #producto.visitas += 1  
    producto.save()  
    return render(request, "detalle_producto.html", {"producto": producto})

def añadir_al_carrito(request, id):
    usuario = request.user if request.user.is_authenticated else None
    
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario)
    
    producto = get_object_or_404(ProductoDb, id=id)
    
    carrito_producto, created = CarritoProductoDB.objects.get_or_create(carrito_fk=carrito, producto_fk=producto)
    if not created:
        carrito_producto.cantidad += 1
        carrito_producto.save()

    return redirect('ver_carrito')

def ver_carrito(request):
    usuario = request.user if request.user.is_authenticated else None
    carrito = CarritoDB.objects.filter(usuario_fk=usuario).first()
    
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito) if carrito else []
    
    return render(request, "ver_carrito.html", {"productos_en_carrito": productos_en_carrito})

# Vista para agregar cantidad
def agregar_cantidad(request, producto_id):
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=None)  # Suponiendo que no hay login
    carrito_producto = get_object_or_404(CarritoProductoDB, producto_fk_id=producto_id, carrito_fk=carrito)
    carrito_producto.cantidad += 1
    carrito_producto.save()
    return redirect('carrito')

# Vista para eliminar producto
def eliminar_producto(request, producto_id):
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=None)
    carrito_producto = get_object_or_404(CarritoProductoDB, producto_fk_id=producto_id, carrito_fk=carrito)
    carrito_producto.delete()
    return redirect('carrito')