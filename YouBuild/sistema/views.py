from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import RegistroUsuarioForm
from django.contrib.auth import login, logout,update_session_auth_hash
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import RegistroUsuarioForm, RegistroProductoForm
from .models import ImagenProductoDB
import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.template.loader import render_to_string

# Vista principal
@login_required
def home_view(request):
    productos = ProductoDb.objects.all().order_by('-visitas')
    carruseles = CarruselDB.objects.all().order_by("id")
    categorias = CategoriaDb.objects.all()
    usuario = request.user.usuariodb
    return render(request, "home.html", {
        "producto": productos,
        "carrusel": carruseles,
        "usuario": usuario,
        'categorias': categorias,
    })

# Perfil de usuario
def perfil_view(request):
    usuario = request.user.usuariodb
    return render(request, "perfil.html",{
      "usuario": usuario,       
    })

# Cerrar sesión
def custom_logout_view(request):
    logout(request)
    return redirect('index')

# Registro de usuario con formulario
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optionally logs in the user after registration
            return redirect('success')  # Redirects to the success page after account creation
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def success(request):
    usuario = request.user.usuariodb  # Assuming `usuariodb` is linked to `user`
    return render(request, 'success.html', {'usuario': usuario})

def terms_and_conditions(request):
    return render(request, 'terms&conditions.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

# Página de inicio
def index_view(request): 
    if request.user.is_authenticated:
        return redirect('home')
    productos = ProductoDb.objects.all().order_by('-visitas')
    carruseles = CarruselDB.objects.all().order_by("id")
    categorias = CategoriaDb.objects.all()
    return render(request, "index.html", {"producto": productos, "carrusel": carruseles, 'categorias': categorias})


# Vista de producto individual
def producto_view(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    producto.visitas += 1
    producto.save()
    
    # Determina la plantilla base según si el usuario está autenticado
    template = 'layoutReg.html' if request.user.is_authenticated else 'layout.html'
    
    # Renderiza la vista con la plantilla seleccionada
    return render(request, "detalle_producto.html", {
        "producto": producto,
        "template": template
    })


# Buscar productos
def buscar_view(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(nombre__icontains=q)
    return render(request, 'index.html', {'producto': productos})

def filtro_productos_view(request):
    # Obtener parámetros de búsqueda del POST
    categoria = request.POST.get('categoria', '')
    precio_min = request.POST.get('precio_min', None)
    precio_max = request.POST.get('precio_max', None)
    ordenar = request.POST.get('ordenar', 'asc')

    # Imprimir los parámetros recibidos
    print("Categoría recibida:", categoria)
    print("Precio mínimo recibido:", precio_min)
    print("Precio máximo recibido:", precio_max)
    print("Ordenar por:", ordenar)

    # Filtrar productos
    productos = ProductoDb.objects.all()
    categorias = CategoriaDb.objects.all()


    # Filtrar por categoría si está presente
    if categoria:
        productos = productos.filter(categoria_fk=categoria)
        print("Productos después de filtrar por categoría:", productos)

    print("Valor de precio_min recibido:", precio_min)
    print("Valor de precio_max recibido:", precio_max)

    # Filtrar por rango de precio
    if precio_min:
        productos = productos.filter(precio__gte=float(precio_min))
        print("Productos después de filtrar por precio mínimo:", productos)

    if precio_max:
        productos = productos.filter(precio__lte=float(precio_max))
        print("Productos después de filtrar por precio máximo:", productos)

    print("Ordenar recibido:", ordenar)

    # Ordenar productos
    if ordenar == 'mayor':
        productos = productos.order_by('-precio')
    elif ordenar == 'menor':
        productos = productos.order_by('precio')
    
    # Imprimir los productos finales después de todos los filtros
    print("Productos después de filtrar y ordenar:", productos)

    # Si es una solicitud AJAX, devolver solo los datos de productos en JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        productos_data = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'imagen': producto.imagenes.first().imagen.url if producto.imagenes.exists() else None,
            }
            for producto in productos
        ]
        
        # Imprimir los datos de productos que se enviarán como respuesta JSON
        print("Datos de productos para respuesta JSON:", productos_data)

        return JsonResponse({'products': productos_data})

    # Para solicitudes normales, renderizar toda la página
    return render(request, 'filtro_productos.html', {
        'productos': productos,
        'categorias': categorias,
    })

# Carrito de compras
@login_required
def carrito_view(request):
    usuario = request.user.usuariodb
    carrito, created = CarritoDB.objects.get_or_create(usuario_fk=usuario)
    carrito_productos = carrito.carritoproductodb_set.select_related('producto_fk')
    carrito_subtotal = sum([item.calcular_subtotal() for item in carrito_productos])
    total = carrito_subtotal
    return render(request, 'Carrito.html', {
        'carrito_productos': carrito_productos,
        'carrito_subtotal': carrito_subtotal,
        'carrito_total': total,
        "usuario": usuario
    })

# Eliminar producto del carrito
@login_required
def eliminar_producto(request, item_id):
    carrito_producto = get_object_or_404(CarritoProductoDB, id=item_id)
    carrito_producto.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('Carrito')

# Actualizar cantidad del carrito
@login_required
def update_cart_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito_producto_id = data.get('item_id')
            nueva_cantidad = int(data.get('quantity'))
            carrito_producto = CarritoProductoDB.objects.filter(id=carrito_producto_id).first()
            if not carrito_producto:
                return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'})
            if nueva_cantidad <= 0:
                carrito_producto.delete()
            else:
                carrito_producto.cantidad = nueva_cantidad
                carrito_producto.save()
            subtotal_producto = carrito_producto.calcular_subtotal()
            carrito_total = carrito_producto.carrito_fk.calcular_total()
            return JsonResponse({'success': True, 'carrito_subtotal': subtotal_producto, 'carrito_total': carrito_total})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Agregar producto al carrito
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id)
    carrito, _ = CarritoDB.objects.get_or_create(usuario_fk=request.user.usuariodb)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito.agregar_producto(producto, cantidad)
    messages.success(request, f"Producto {producto.nombre} agregado al carrito.")
    return redirect('Carrito')

# Cantidad de productos en el carrito
def get_cart_count(request):
    cart_count = request.session.get('cart_count', 0)
    return JsonResponse({'cart_count': cart_count})

# Cargar provincias en AJAX
def cargar_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)

# Cargar municipios en AJAX
def cargar_municipios(request):
    provincia_id = request.GET.get('provincia_id')
    municipios = MunicipioDB.objects.filter(provincia_fk=provincia_id).order_by('nombre')
    return JsonResponse(list(municipios.values('id', 'nombre')), safe=False)

# Vista de prueba
def test(request):
    return render(request, "pagina.html")

# Vista de creación de cuenta (no se está usando, puede eliminarse)
def crear_cuenta_view(request):
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
@login_required     
def perfil_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance= request.user.usuariodb)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Tu cuenta ha sido actualizada')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.usuariodb)
    
    context = {    
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request,'perfil.html',context)
# Registro de producto
@login_required
def registro_producto(request):
    if request.method == 'POST':
        form = RegistroProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False) 
            producto.usuario_fk = request.user.usuariodb  
            producto.save() 
            imagenes = request.FILES.getlist('imagenes')  
            for imagen in imagenes:
                ImagenProductoDB.objects.create(producto_fk=producto, imagen=imagen)
            
            return redirect('home') 
    else:
        form = RegistroProductoForm()
    return render(request, 'registro_producto.html', {'form': form})

@login_required
def vender_view(request):
    return redirect('registro_producto')

@login_required
def ver_lista_favoritos(request):
    usuario = request.user.usuariodb  # Obtiene el perfil de usuario
    lista_favoritos_items = ListaFavoritosDB.objects.filter(usuario=usuario)
    
    return render(request, 'listaFavoritos.html', {
        'lista_favoritos_items': lista_favoritos_items,
        'usuario': usuario  # Pasa el usuario al contexto de la plantilla
    })

@login_required
def agregar_a_lista_favoritos(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id)
    favoritos = ListaFavoritosDB(usuario=request.user.usuariodb)
    favoritos.agregar_producto(producto)  # Utiliza el nuevo método para agregar
    return redirect('listaFavoritos')

@login_required
def eliminar_de_lista_favoritos(request, producto_id):
    usuario = request.user.usuariodb
    producto = get_object_or_404(ProductoDb, id=producto_id)  # Obtén el producto para eliminarlo
    favoritos = ListaFavoritosDB(usuario=usuario)  # Crea una instancia de ListaFavoritosDB
    favoritos.eliminar_producto(producto)  # Utiliza el nuevo método para eliminar
    return redirect('listaFavoritos')
