from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User 
from .forms import RegistroUsuarioForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .models import *
from .forms import RegistroUsuarioForm, RegistroProductoForm
from .models import ImagenProductoDB
import json
from django.shortcuts import render
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import secrets

# Vista principal
@login_required
def home_view(request):
    request.session['productos_busqueda'] = None

    # Todos los productos y los que están en promoción
    productos, productos_oferta = obtener_productos_oferta()
    productos = ProductoDb.objects.all().order_by('-visitas')

    # Carruseles y categorías
    carruseles = CarruselDB.objects.all().order_by("id")
    categorias = CategoriaDb.objects.all()

    usuario = request.user.usuariodb
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = ListaFavoritosDB.objects.filter(usuario=request.user.usuariodb).values_list('producto_id', flat=True)
        print("Productos en favoritos:", list(favoritos_ids))

    return render(request, "home.html", {
        "producto": productos,
        "productos_oferta": productos_oferta,
        "carrusel": carruseles,
        "usuario": usuario,
        "categorias": categorias,
        "favoritos_ids": favoritos_ids,
    })


def perfil_view(request):
    usuario = request.user.usuariodb
    return render(request, "perfil.html",{
      "usuario": usuario,       
    })




def custom_logout_view(request):
    logout(request)
    return redirect('index')

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'email_exists': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('success')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def success(request):
    usuario = request.user.usuariodb  
    return render(request, 'success.html', {'usuario': usuario})

def terms_and_conditions(request):
    return render(request, 'terms&conditions.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

# Página de inicio para usuarios no autenticados
def index_view(request): 
    if request.user.is_authenticated:
        return redirect('home')

    # Todos los productos y los que están en promoción
    productos, productos_oferta = obtener_productos_oferta()
    productos = ProductoDb.objects.all().order_by('-visitas')

    # Carruseles y categorías
    carruseles = CarruselDB.objects.all().order_by("id")
    categorias = CategoriaDb.objects.all()
    favoritos_ids = []

    if request.user.is_authenticated:
        favoritos_ids = ListaFavoritosDB.objects.filter(usuario=request.user.usuariodb).values_list('producto_id', flat=True)
        print("Productos en favoritos:", list(favoritos_ids))

    return render(request, "index.html", {
        "producto": productos,
        "productos_oferta": productos_oferta,
        "carrusel": carruseles,
        "categorias": categorias,
        "favoritos_ids": favoritos_ids,
    })
def obtener_productos_oferta():
    productos = ProductoDb.objects.all().order_by('-visitas')
    productos_oferta = [producto for producto in productos if producto.esta_en_promocion()]
    return productos, productos_oferta

def lista_productosOfert(request):
    # Importamos el método para obtener los productos y las ofertas
    productos, productos_oferta = obtener_productos_oferta()

    # Determinamos la plantilla base según si el usuario está autenticado
    layout_template = 'layoutReg.html' if request.user.is_authenticated else 'layout.html'

    # Renderizamos la vista con la plantilla base y los productos/ofertas como parte del contexto
    return render(request, 'ListaProductOferta.html', {
        'productos': productos,
        'productos_oferta': productos_oferta,
        'layout_template': layout_template,  # Pasamos el layout base según el estado del usuario
    })



def producto_view(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    producto.visitas += 1
    producto.save()
    productoRel = ProductoDb.objects.filter(nombre__icontains=producto.nombre)

    # Calcular datos dinámicos
    precio_final = producto.precio_final()
    descuento_aplicado = producto.descuento if producto.esta_en_promocion() else 0
    tiempo_restante = producto.tiempo_restante_promocion()  # Tiempo restante en segundos

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = ListaFavoritosDB.objects.filter(usuario=request.user.usuariodb).values_list('producto_id', flat=True)

    template = 'layoutReg.html' if request.user.is_authenticated else 'layout.html'
    
    return render(request, "detalle_producto.html", {
        "producto": producto,
        "precio_final": precio_final,
        "descuento_aplicado": descuento_aplicado,
        "tiempo_restante": tiempo_restante,  # Tiempo en segundos para el frontend
        "template": template,
        "favoritos_ids": favoritos_ids,
        "relacionados": productoRel,
    })
# Buscar productos
def buscar_view(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(nombre__icontains=q)
    categorias = CategoriaDb.objects.all()
    favoritos_ids = []
    pag = 'index.html'
    if request.user.is_authenticated:
        pag = 'home.html'
        favoritos_ids = ListaFavoritosDB.objects.filter(usuario=request.user.usuariodb).values_list('producto_id', flat=True)
        print("Productos en favoritos:", list(favoritos_ids))

    # Guardar los IDs de los productos de la búsqueda en la sesión
    request.session['productos_busqueda'] = [producto.id for producto in productos]
    
    return render(request, pag, {'producto': productos, 'categorias': categorias, "favoritos_ids": favoritos_ids,})

def filtro_productos_view(request):
    # Obtener los IDs de los productos de la búsqueda almacenados en la sesión
    productos_busqueda_ids = request.session.get('productos_busqueda', None)
    
    # Obtener la lista inicial de productos con base en la búsqueda o todos si no hubo búsqueda
    if productos_busqueda_ids:
        productos = ProductoDb.objects.filter(id__in=productos_busqueda_ids)
    else:
        productos = ProductoDb.objects.all().order_by('-visitas')
    
    categorias = CategoriaDb.objects.all()

    # Obtener parámetros de búsqueda del POST
    categoria = request.POST.get('categoria', '')
    precio_min = request.POST.get('precio_min', None)
    precio_max = request.POST.get('precio_max', None)
    ordenar = request.POST.get('ordenar', 'asc')
    oferta = request.POST.get('oferta', '')  # El filtro de solo ofertas

    # Filtrar por categoría si es que se seleccionó una
    if categoria:
        productos = productos.filter(categoria_fk=categoria)
        print("Productos después de filtrar por categoría:", productos)

    # Filtrar por rango de precio
    if precio_min:
        productos = productos.filter(precio__gte=float(precio_min))
        print("Productos después de filtrar por precio mínimo:", productos)

    if precio_max:
        productos = productos.filter(precio__lte=float(precio_max))
        print("Productos después de filtrar por precio máximo:", productos)

    # Filtrar por "oferta" (productos en promoción)
    if oferta == 'si':
        productos = productos.filter(estado='promocion')  # Filtramos solo productos en promoción
        print("Productos después de filtrar por solo ofertas:", productos)
    elif oferta == 'no':
        # No aplicar ningún filtro de oferta, mostramos todos los productos
        pass

    # Ordenar productos
    if ordenar == 'mayor':
        productos = productos.order_by('-precio')
    elif ordenar == 'menor':
        productos = productos.order_by('precio')
    elif ordenar == 'relevantes':
        productos = productos.order_by('-visitas')
    
    print("Productos después de filtrar y ordenar:", productos)

    # Si no se seleccionó ningún filtro, mostrar todos los productos
    if categoria == '' and precio_min is None and precio_max is None and ordenar == 'asc' and oferta == '':
        productos = ProductoDb.objects.all().order_by('-visitas')

    # Si es una solicitud AJAX, devolver solo los datos de productos en JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        productos_data = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'precio_final': producto.precio_final(),  # Llamar al método para obtener el precio con descuento
                'imagen': producto.imagenes.first().imagen.url if producto.imagenes.exists() else None,
                'estado': producto.estado,  # Puedes incluir el estado para identificar si está en promoción
                'descuento': producto.descuento,  # Incluir el porcentaje de descuento si deseas usarlo en el frontend
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
    })


@login_required
def eliminar_producto(request, item_id):
    carrito_producto = get_object_or_404(CarritoProductoDB, id=item_id)
    carrito_producto.delete()
    return redirect('Carrito')


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


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id)
    carrito, _ = CarritoDB.objects.get_or_create(usuario_fk=request.user.usuariodb)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito.agregar_producto(producto, cantidad)
    return redirect('Carrito')

def get_cart_count(request):
    usuario = request.user.usuariodb
    cart_count = CarritoProductoDB.objects.filter(carrito_fk__usuario_fk=usuario).aggregate(total_quantity=Sum('cantidad'))['total_quantity'] or 0
    return JsonResponse({'cart_count': cart_count})


def cargar_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)


def cargar_municipios(request):
    provincia_id = request.GET.get('provincia_id')
    municipios = MunicipioDB.objects.filter(provincia_fk=provincia_id).order_by('nombre')
    return JsonResponse(list(municipios.values('id', 'nombre')), safe=False)


def test(request):
    return render(request, "pagina.html")


@login_required
def update_profile_photo(request):
    if request.method == 'POST' and 'imagen_perfil' in request.FILES:
        imagen = request.FILES['imagen_perfil']
        extension = imagen.name.split('.')[-1].lower()
        allowed_extensions = ['png', 'jpg', 'jpeg']
        if extension not in allowed_extensions:
            messages.error(request, "Formato no permitido")
            return redirect('profile')  # Redirigir a la página de perfil sin guardar la imagen
        usuario_db = request.user.usuariodb
        usuario_db.imagen_perfil = imagen
        usuario_db.save()
        messages.success(request, "Tu foto de perfil ha sido actualizada con éxito.")
        return redirect('profile')
    
    # Redirigir a la página de perfil si no es una solicitud POST
    return redirect('profile')



@login_required
def perfil_view(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.usuariodb)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile_update':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.usuariodb)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, '¡Tus datos personales han sido actualizados!')
                return redirect('profile')
            else:
                print("User form errors:", u_form.errors)
                print("Profile form errors:", p_form.errors)

        elif form_type == 'password_change':
            # Verificar si el usuario está bloqueado
            if request.user.usuariodb.esta_bloqueado:
                tiempo_restante = (request.user.usuariodb.bloqueo_password_hasta - timezone.now()).seconds // 3600
                messages.error(request, f'Demasiados intentos fallidos, inténtelo nuevamente en {tiempo_restante} horas.', extra_tags='danger')
            else:
                password_form = PasswordChangeForm(user=request.user, data=request.POST)
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                    messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
                    # Restablecer intentos después de un cambio exitoso
                    request.user.usuariodb.restablecer_intentos()
                    return redirect('profile')
                else:
                    # Incrementar intentos fallidos si la contraseña es incorrecta
                    request.user.usuariodb.incrementar_intentos_fallidos()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'password_form': password_form
    }
    return render(request, 'perfil.html', context)


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
            
            return redirect('confirmacion_producto')  # Redirigir a la página de confirmación
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
        'usuario': usuario  
    })

@login_required
def agregar_a_lista_favoritos(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(ProductoDb, id=producto_id)
        favoritos, created = ListaFavoritosDB.objects.get_or_create(
            usuario=request.user.usuariodb, 
            producto=producto
        )

        if not created:  # Ya existía, así que lo eliminamos
            favoritos.delete()
            en_favoritos = False
        else:
            en_favoritos = True

        return JsonResponse({'enFavoritos': en_favoritos, 'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def eliminar_de_lista_favoritos(request, producto_id):
    usuario = get_object_or_404(UsuarioDB, id=request.user.id)
    try:
        # Intenta obtener el objeto ListaFavoritosDB que coincida con usuario y producto_id
        favorito = ListaFavoritosDB.objects.get(usuario=usuario, producto_id=producto_id)
        favorito.delete()  # Elimina el objeto si existe
        messages.success(request, "Producto eliminado de tu lista de favoritos.")
    except ListaFavoritosDB.DoesNotExist:
        # Si no se encuentra el favorito, muestra un mensaje de error
        messages.error(request, "El producto no está en tu lista de favoritos.")

    return redirect('listaFavoritos')

def confirmacion_producto(request):
    return render(request, 'confirmacion_producto.html')

@login_required
def publicaciones_usuario_view(request):
    usuario = request.user.usuariodb  # Obtiene el perfil de usuario
    productos = ProductoDb.objects.filter(usuario_fk=usuario)
    
    return render(request, "Mis_publiccaciones.html", {
        'mis_productos': productos,
        'usuario': usuario  
    })
    
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id, usuario_fk=request.user.usuariodb)
    imagenes_actuales = ImagenProductoDB.objects.filter(producto_fk=producto)
    
    if request.method == 'POST':
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario_fk = request.user.usuariodb  # Asegurarse de que el producto pertenezca al usuario
            producto.save()
            
            # Si se suben nuevas imágenes, las eliminamos y las guardamos
            if 'imagenes' in request.FILES:
                ImagenProductoDB.objects.filter(producto_fk=producto).delete()  # Eliminar las imágenes previas
                imagenes = request.FILES.getlist('imagenes')
                for imagen in imagenes:
                    ImagenProductoDB.objects.create(producto_fk=producto, imagen=imagen)

            return redirect('confirmacion_producto')  # Redirigir a la página de confirmación
    else:
        form = EditarProductoForm(instance=producto)

    return render(request, 'edit_producto.html', {'form': form, 'editar': True, 'imagenes_actuales': imagenes_actuales})

@login_required
def actualizar_descuento_view(request):
    # Asegurarse de que el usuario tiene productos asociados
    usuario = request.user.usuariodb
    productos = ProductoDb.objects.filter(usuario_fk=usuario)  # Productos del usuario

    if request.method == 'POST':
        # Recuperar el id del producto, descuento y fechas desde el POST
        producto_id = request.POST.get('producto_id')
        descuento = request.POST.get('descuento')
        fecha_inicio = request.POST.get('fecha_inicio_promocion')
        fecha_fin = request.POST.get('fecha_fin_promocion')

        if not producto_id or not descuento:
            return render(request, 'crear_oferta.html', {
                'productos': productos,
                'error': 'Debe seleccionar un producto y un descuento.'
            })

        # Asegurarse de que el descuento sea un número válido
        try:
            descuento = float(descuento)
        except ValueError:
            return render(request, 'crear_oferta.html', {
                'productos': productos,
                'error': 'El descuento debe ser un número válido.'
            })

        if descuento < 0 or descuento > 100:
            return render(request, 'crear_oferta.html', {
                'productos': productos,
                'error': 'El descuento debe estar entre 0 y 100.'
            })

        # Validar las fechas
        try:
            if fecha_inicio:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M')  # Asegúrate de que el formato coincida
            if fecha_fin:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M')  # Asegúrate de que el formato coincida
        except ValueError:
            return render(request, 'crear_oferta.html', {
                'productos': productos,
                'error': 'Las fechas deben tener un formato válido (YYYY-MM-DD HH:MM).'
            })

        # Actualizar el producto con descuento y fechas
        producto = get_object_or_404(ProductoDb, id=producto_id, usuario_fk=usuario)
        producto.descuento = descuento
        producto.fecha_inicio_promocion = fecha_inicio
        producto.fecha_fin_promocion = fecha_fin
        producto.save()

        messages.success(request, 'Descuento y fechas de promoción actualizados con éxito.')

        # Redirigir a "mis publicaciones"
        return redirect('mis_publicaciones')

    return render(request, 'crear_oferta.html', {'productos': productos})