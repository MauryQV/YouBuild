from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import ProductoDb, CategoriaDb, CarruselDB, UsuarioDB, CarritoProductoDB, CarritoDB

# Vista principal
def IndexView(request): 
    productos = ProductoDb.objects.all().order_by("id")  
    carruseles = CarruselDB.objects.all().order_by("id")
    return render(request, "index.html", {"producto": productos, "carrusel": carruseles})

def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    imagenes = producto.imagenes.all()
    return render(request, "detalle_producto.html", {"producto": producto})

def BuscarView(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(nombre__icontains=q)
    print('Estos son los productos:')
    for producto in productos:
        print(producto)
    return render(request, 'index.html', {'producto': productos})

def CheckoutView(request):
    return render(request, "layout.html")

def carrito_view(request):
    usuario_prueba = get_object_or_404(UsuarioDB, id=1)
    carrito = get_object_or_404(CarritoDB, usuario_fk=usuario_prueba)
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)
    
    # Calcular subtotal
    carrito_subtotal = sum(item.producto_fk.precio * item.cantidad for item in productos_en_carrito)

    return render(request, 'Carrito.html', {
        'productos': productos_en_carrito,
        'carrito_subtotal': carrito_subtotal,
        'carrito_total': carrito_subtotal  # Cambia esto si agregas costos de envío
    })



def eliminar_producto(request, item_id):
    if request.method == 'POST':
        # Obtener el producto del carrito usando el ID
        producto = get_object_or_404(CarritoProductoDB, id=item_id)
        
        # Eliminar el producto del carrito
        producto.delete()
        
        # Redirigir de vuelta al carrito
        return redirect('Carrito')

