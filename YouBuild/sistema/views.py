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
    # Obtener el usuario con id=1
    usuario_prueba = get_object_or_404(UsuarioDB, id=1)
    
    # Obtener el carrito del usuario
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)

    # Calcular el subtotal del carrito
    carrito_subtotal = sum(item.producto_fk.precio * item.cantidad for item in productos_en_carrito)
    total = carrito_subtotal  # O aplicar impuestos, descuentos, etc.

    # Preparar el contexto con los datos del usuario
    context = {
        'productos': productos_en_carrito,
        'carrito_subtotal': carrito_subtotal,
        'total': total,
        'usuario': usuario_prueba
    }

    # Solo permitir el paso a la confirmación si hay productos en el carrito
    if not productos_en_carrito.exists():
        return redirect('Carrito')  # Redirigir al carrito si está vacío

    return render(request, 'confirmacion.html', context)


def eliminar_producto(request, item_id):
    if request.method == 'POST':
        try:
            # Obtener el producto del carrito usando el ID
            producto = get_object_or_404(CarritoProductoDB, id=item_id)

            # Eliminar el producto del carrito
            producto.delete()

            # Actualizar el conteo del carrito en la sesión
            cart = request.session.get('cart', {})
            if str(producto.producto_fk.id) in cart:
                del cart[str(producto.producto_fk.id)]
                request.session['cart'] = cart
                request.session['cart_count'] = sum(item['quantity'] for item in cart.values())

            # Redirigir a la página del carrito en lugar de devolver JSON
            return redirect('Carrito')  # Aquí asume que 'Carrito' es el nombre de la vista que muestra el carrito
        except CarritoProductoDB.DoesNotExist:
            # Manejar si el producto no se encuentra en el carrito
            return redirect('Carrito')  # Redirigir de vuelta al carrito si hay un error

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

@csrf_exempt  # Disable CSRF for this view
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        # Fetch the product from the database
        producto = get_object_or_404(ProductoDb, id=producto_id)

        # Update session cart for counting
        cart = request.session.get('cart', {})

        # Check if the product is already in the session cart
        if str(producto_id) in cart:
            cart[str(producto_id)]['quantity'] += 1  # Increment quantity
        else:
            # Add new product to session cart
            cart[str(producto_id)] = {
                'name': producto.nombre,
                'price': producto.precio,
                'quantity': 1
            }

        # Save the updated cart in the session
        request.session['cart'] = cart
        request.session['cart_count'] = sum(item['quantity'] for item in cart.values())

        # Handle the database cart (CarritoDB)
        # In this example, we're adding it to both the session and the database
        usuario_prueba = get_object_or_404(UsuarioDB, id=1)  # Replace this with the appropriate user logic
        carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)
        carrito_producto, created = CarritoProductoDB.objects.get_or_create(carrito_fk=carrito, producto_fk=producto)

        # Check stock and add to the database cart
        if carrito_producto.cantidad <= producto.cantidad:
            carrito_producto.save()

            # Redirect the user to the 'carrito' page after adding
            return JsonResponse({
                'success': True,
                'message': 'Producto agregado correctamente.',
                'redirect_url': '/carrito/'  # Adjust this to the actual URL for your carrito page
            })
        else:
            return JsonResponse({'success': False, 'message': 'No hay suficiente stock disponible.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def get_cart_count(request):
    cart_count = request.session.get('cart_count', 0)
    return JsonResponse({'cart_count': cart_count})

def obtener_direccion_usuario(request):
    # Obtener el usuario con id=1
    usuario_prueba = get_object_or_404(UsuarioDB, id=1)

    # Obtener información de dirección
    municipio = usuario_prueba.municipio_fk
    provincia = municipio.provincia_fk if municipio else None
    departamento = provincia.departamento_fk if provincia else None

    # Crear un diccionario con los datos que quieres enviar
    data = {
        'municipio': municipio.nombre if municipio else 'No especificado',
        'provincia': provincia.nombre if provincia else 'No especificado',
        'departamento': departamento.nombre if departamento else 'No especificado',
    }

    # Devolver los datos en formato JSON
    return JsonResponse(data)

def compra_directa_view(request, producto_id):
    if request.method == 'POST':
        # Obtener el producto
        producto = get_object_or_404(ProductoDb, id=producto_id)
        
        # Obtener el usuario de prueba (luego deberías cambiar esto cuando implementes autenticación)
        usuario_prueba = get_object_or_404(UsuarioDB, id=1)

        # Crear o recuperar el carrito del usuario
        carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario_prueba)

        # Agregar el producto al carrito con una cantidad de 1
        carrito_producto, created = CarritoProductoDB.objects.get_or_create(
            carrito_fk=carrito, 
            producto_fk=producto,
            defaults={'cantidad': 1}
        )

        # Si el producto ya estaba en el carrito, aumentar la cantidad
        if not created:
            carrito_producto.cantidad += 1
            carrito_producto.save()

        # Redirigir a la página de confirmación
        return JsonResponse({
            'success': True,
            'redirect_url': '/confirmacion/'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})