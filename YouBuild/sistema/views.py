from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import RegistroUsuarioForm
from django.contrib.auth import login, logout
from django.contrib import messages
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UsuarioDBSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

@login_required
def home_view(request):
    productos = ProductoDb.objects.all().order_by('-visitas')
    carruseles = CarruselDB.objects.all().order_by("id")
    # Obtenemos el perfil del usuario logueado
    usuario = request.user.usuariodb

    return render(request, "home.html", {
        "producto": productos,
        "carrusel": carruseles,
        "usuario": usuario  # Pasamos el perfil del usuario al contexto
    })


def perfil_view(request):
    return render(request, "perfil.html")

def custom_logout_view(request):
    logout(request)  # Cierra la sesión
    return redirect('index') 

#CON FORMS.PY
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)  # Agregar request.FILES
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

    
def index_view(request): 
    # Redirigir a /home si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('home')
    
    # En caso contrario, mostrar la página de inicio para usuarios no autenticados
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

@login_required
def carrito_view(request):
    user = request.user

    # Verificar si el usuario tiene el objeto Usuariodb, de lo contrario crearlo
    try:
        usuario = user.usuariodb
    except UsuarioDB.DoesNotExist:
        # Si no existe el usuariodb, redirigir o crearlo automáticamente
        usuario = UsuarioDB.objects.create(user=user)
    
    # Obtener o crear el carrito para el usuario
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario)
    usuario = request.user.usuariodb

    # Obtener los productos del carrito
    carrito_productos = carrito.carritoproductodb_set.select_related('producto_fk')

    # Calcular subtotal y total
    carrito_subtotal = sum([item.calcular_subtotal() for item in carrito_productos])
    total = carrito_subtotal  # Si no hay otros cargos adicionales

    context = {
        'carrito_productos': carrito_productos,
        'carrito_subtotal': carrito_subtotal,
        'carrito_total': total,
        "usuario": usuario  # Pasamos el perfil del usuario al contexto
    }

    return render(request, 'Carrito.html', context)


@login_required
def eliminar_producto(request, item_id):
    carrito_producto = get_object_or_404(CarritoProductoDB, id=item_id)
    carrito = carrito_producto.carrito_fk
    carrito.eliminar_producto(carrito_producto.producto_fk)

    messages.success(request, "Producto eliminado del carrito.")
    return redirect('Carrito')



@login_required
def update_cart_quantity(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)  
            
            # Get the 'item_id' and 'quantity' from the request
            carrito_producto_id = data.get('item_id')  # Ensure this is the ID of CarritoProductoDB, not ProductoDb
            nueva_cantidad = int(data.get('quantity'))

            # Find the CarritoProductoDB object using 'carrito_producto_id'
            carrito_producto = CarritoProductoDB.objects.filter(id=carrito_producto_id).first()
            
            # If no such item exists in the cart
            if not carrito_producto:
                return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'})
            
            # Update the quantity or remove the product if the quantity is <= 0
            if nueva_cantidad <= 0:
                carrito_producto.delete()  # Remove the product from the cart if the quantity is 0 or less
            else:
                carrito_producto.cantidad = nueva_cantidad
                carrito_producto.save()

            # Recalculate totals for the cart
            carrito = carrito_producto.carrito_fk
            subtotal_producto = carrito_producto.calcular_subtotal()
            carrito_total = carrito.calcular_total()

            return JsonResponse({
                'success': True,
                'carrito_subtotal': subtotal_producto,
                'carrito_total': carrito_total
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})




@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id)
    carrito, _ = CarritoDB.objects.get_or_create(usuario_fk=request.user.usuariodb)

    # La cantidad puede venir desde el formulario o puede ser 1 por defecto
    cantidad = int(request.POST.get('cantidad', 1))

    # Agregar el producto al carrito
    carrito.agregar_producto(producto, cantidad)

    return redirect('Carrito')


def success(request):
    return render(request, 'success.html')


def get_cart_count(request):
    cart_count = request.session.get('cart_count', 0)
    return JsonResponse({'cart_count': cart_count})

def cargar_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)

# Vista para obtener municipios según la provincia
def cargar_municipios(request):
    provincia_id = request.GET.get('provincia_id')
    municipios = MunicipioDB.objects.filter(provincia_fk=provincia_id).order_by('nombre')
    return JsonResponse(list(municipios.values('id', 'nombre')), safe=False)

def test(request):
    return render(request, "pagina.html")


def CrearCuentaView(request):
    return render(request, 'CrearCuenta.html')

# Create your views here.
"""class RegisterUserAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Permitir archivos en la solicitud

    def post(self, request):
        serializer = UsuarioDBSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
    
