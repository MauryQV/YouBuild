from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductoDb, CategoriaDb, CarruselDB, UsuarioDB, CarritoProductoDB, CarritoDB

# Vista principal
def IndexView(request): 
    productos = ProductoDb.objects.all().order_by('-visitas')  
    carruseles = CarruselDB.objects.all().order_by("id")
    return render(request, "index.html", {"producto": productos, "carrusel": carruseles})


def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    producto.visitas += 1  
    producto.save()  
    imagenes = producto.imagenes.all()  # Línea adicional si necesitas imágenes relacionadas
    return render(request, "detalle_producto.html", {"producto": producto})

def BuscarView(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(nombre__icontains=q)
    print('Estos son los productos:')
    for producto in productos:
        print(producto)
    return render(request, 'index.html', {'producto': productos})

def CheckoutView(request):
    return render(request, "checkout.html")  # Asegúrate de que checkout.html esté en la carpeta de plantillas

def carrito_view(request):
    usuario_prueba = get_object_or_404(UsuarioDB, id=1)
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)

    for item in productos_en_carrito:
        item.subtotalp = item.producto_fk.precio * item.cantidad  # Calcular subtotal por producto

    # Calcular el subtotal y total del carrito
    carrito_subtotal = sum(item.subtotalp for item in productos_en_carrito)
    
    # Renderiza el template con los productos en el carrito
    return render(request, 'Carrito.html', {
        'productos': productos_en_carrito,
        'carrito_subtotal': carrito_subtotal,
        'carrito_total': carrito_subtotal
    })
    
def confirmacion_view(request):
    usuario_prueba = get_object_or_404(UsuarioDB, id=1)
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)
    carrito_subtotal = sum(item.producto_fk.precio * item.cantidad for item in productos_en_carrito)
    total = carrito_subtotal  # O aplicar impuestos, descuentos, etc.

    context = {
        'productos': productos_en_carrito,
        'carrito_subtotal': carrito_subtotal,
        'total': total,
    }

    # Solo permitir el paso a la confirmación si hay productos en el carrito
    if not productos_en_carrito.exists():
        return redirect('Carrito')  # Redirigir al carrito si está vacío

    return render(request, 'checkout.html', context)


def eliminar_producto(request, item_id):
    if request.method == 'POST':
        # Obtener el producto del carrito usando el ID
        producto = get_object_or_404(CarritoProductoDB, id=item_id)
        
        # Eliminar el producto del carrito
        producto.delete()
        
        # Redirigir de vuelta al carrito
        return redirect('Carrito')

@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        new_quantity = data.get('quantity')
        carrito_producto = CarritoProductoDB.objects.filter(id=item_id).first()
        if carrito_producto:
            # Verificar que la nueva cantidad no exceda el stock del producto
            if new_quantity <= carrito_producto.producto_fk.cantidad:
                if new_quantity > 0:
                    carrito_producto.cantidad = new_quantity
                    carrito_producto.save()
                else:
                    carrito_producto.delete()  # Elimina el producto si la cantidad es 0

                # Calcular subtotal actualizado para el producto
                new_subtotal = carrito_producto.cantidad * carrito_producto.producto_fk.precio

                # Calcular el total actualizado para el carrito
                carrito_total = sum(
                    item.cantidad * item.producto_fk.precio for item in CarritoProductoDB.objects.filter(carrito_fk=carrito_producto.carrito_fk)
                )

                return JsonResponse({"success": True, "new_subtotal": new_subtotal, "new_total": carrito_total})
            else:
                return JsonResponse({"success": False, "message": "No hay suficiente stock disponible."})

    return JsonResponse({"success": False, "message": "Error al actualizar el carrito."})


def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        usuario_prueba = get_object_or_404(UsuarioDB, id=1)
        carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)
        producto = get_object_or_404(ProductoDb, id=producto_id)
        carrito_producto, created = CarritoProductoDB.objects.get_or_create(carrito_fk=carrito, producto_fk=producto)

        if carrito_producto.cantidad <= producto.cantidad:
            carrito_producto.save()
            
            return JsonResponse({'success': True, 'message': 'Producto agregado correctamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'No hay suficiente stock disponible.'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido.'})

