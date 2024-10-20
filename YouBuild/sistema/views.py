from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductoDb, CategoriaDb, CarruselDB, UsuarioDB, CarritoProductoDB, CarritoDB
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import F

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguear al usuario tras registrarlo
            return redirect('index')  # Redirigir a la página principal
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirige si ya está autenticado
        return super().dispatch(request, *args, **kwargs)

    
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

@login_required(login_url='/login/')
def carrito_view(request):
    usuario = request.user.usuariodb
    carrito = CarritoDB.objects.filter(usuario_fk=usuario).first()
    carrito_productos = carrito.carritoproductodb_set.all() if carrito else []
    carrito_subtotal = sum([item.calcular_subtotal() for item in carrito_productos])

    total = carrito.calcular_total() if carrito else 0

    context = {
        'carrito_productos': carrito_productos,
        'carrito_subtotal': carrito_subtotal,
        'total': total,
    }
    return render(request, 'Carrito.html', context)
    
    
@login_required
def confirmacion_view(request):
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=request.user.usuariodb)
    productos_en_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)

    carrito_subtotal = sum(item.producto_fk.precio * item.cantidad for item in productos_en_carrito)
    total = carrito_subtotal

    context = {
        'productos': productos_en_carrito,
        'carrito_subtotal': carrito_subtotal,
        'total': total,
        'usuario': request.user.usuariodb
    }

    if not productos_en_carrito.exists():
        return redirect('Carrito')

    return render(request, 'confirmacion.html', context)

@login_required
def eliminar_producto(request, item_id):
    carrito_producto = get_object_or_404(CarritoProductoDB, id=item_id)
    carrito_producto.delete()

    messages.success(request, "Producto eliminado del carrito.")
    return redirect('Carrito')



@login_required
def update_cart_quantity(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nueva_cantidad = int(request.POST.get('cantidad'))

        producto = get_object_or_404(ProductoDb, id=producto_id)
        usuario = request.user.usuariodb
        carrito = get_object_or_404(CarritoDB, usuario_fk=usuario)

        carrito_producto = get_object_or_404(CarritoProductoDB, carrito_fk=carrito, producto_fk=producto)
        carrito_producto.cantidad = nueva_cantidad
        carrito_producto.save()

        messages.success(request, "Cantidad actualizada.")
        return redirect('Carrito')

@login_required
def agregar_al_carrito(request, producto_id):
    # Obtener el producto a partir del ID proporcionado
    producto = get_object_or_404(ProductoDb, id=producto_id)
    usuario = request.user.usuariodb

    # Verificar si el usuario ya tiene un carrito o crear uno nuevo
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario)

    # Verificar si el producto ya está en el carrito
    carrito_producto, created = CarritoProductoDB.objects.get_or_create(
        carrito_fk=carrito, producto_fk=producto)

    if not created:
        # Si el producto ya está en el carrito, incrementar la cantidad
        carrito_producto.cantidad = F('cantidad') + 1
        carrito_producto.save()

    messages.success(request, "Producto agregado al carrito.")
    return redirect('Carrito')


def get_cart_count(request):
    cart_count = request.session.get('cart_count', 0)
    return JsonResponse({'cart_count': cart_count})

"""
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
"""
def test(request):
    return render(request, "pagina.html")