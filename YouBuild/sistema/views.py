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
import base64
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

# Vista principal
@login_required
def home_view(request):
    request.session['productos_busqueda'] = None

    # Actualizar estados de promociones antes de cargar los productos
    actualizar_estados_promociones(request)
    # Todos los productos y los que están en promoción
    productos, productos_oferta = obtener_productos_oferta()
    productos = ProductoDb.objects.filter(cantidad__gt=0).order_by('-visitas')

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

def obtener_productos_oferta():
    # Filtra los productos generales
    productos = ProductoDb.objects.filter(cantidad__gt=0).order_by('-visitas')

    # Filtra los productos en oferta (ajusta el filtro según cómo determines qué es una oferta)
    productos_oferta = ProductoDb.objects.filter(cantidad__gt=0, en_oferta=True).order_by('-visitas')

    return productos, productos_oferta

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
    productos = ProductoDb.objects.filter(cantidad__gt=0).order_by('-visitas')


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

    # Filtrar productos relacionados por categoría y excluir el producto actual
    productoRel = ProductoDb.objects.filter(
        categoria_fk=producto.categoria_fk
    ).exclude(id=producto.id).select_related('categoria_fk').prefetch_related('imagenes')[:6]

    # Calcular datos dinámicos
    precio_final = producto.precio_final()
    descuento_aplicado = producto.descuento if producto.esta_en_promocion() else 0
    tiempo_restante = producto.tiempo_restante_promocion()  # Tiempo restante en segundos

    # Productos relacionados (misma categoría, excluyendo el producto actual)
    productos_relacionados = ProductoDb.objects.filter(
        categoria_fk=producto.categoria_fk, disponible=True
    ).exclude(id=producto.id)[:4]  # Mostrar hasta 4 productos

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
        "productos_relacionados": productos_relacionados,  # Pasar productos relacionados al template
    })

from django.http import JsonResponse

@login_required
def actualizar_estados_promociones(request):
    """
    Actualiza el estado de todos los productos en promoción que hayan expirado.
    """
    productos = ProductoDb.objects.filter(estado='promocion')  # Filtra productos en promoción
    total_actualizados = 0

    for producto in productos:
        if producto.fecha_fin_promocion and timezone.now() > producto.fecha_fin_promocion:
            producto.actualizar_estado()
            total_actualizados += 1

    # Retorna el resultado en formato JSON para mayor flexibilidad
    return JsonResponse({
        'success': True,
        'productos_actualizados': total_actualizados,
        'mensaje': f"Se actualizaron {total_actualizados} productos."
    })

def buscar_view(request):
    q = request.GET.get('q', '')
    productos = ProductoDb.objects.filter(cantidad__gt=0, nombre__icontains=q)
    categorias = CategoriaDb.objects.all()
    favoritos_ids = []
    
    # Seleccionar plantilla base dependiendo del estado de autenticación
    templateB = 'layoutReg.html' if request.user.is_authenticated else 'layout.html'
    
    # Obtener los favoritos si el usuario está autenticado
    if request.user.is_authenticated:
        favoritos_ids = ListaFavoritosDB.objects.filter(usuario=request.user.usuariodb).values_list('producto_id', flat=True)
        print("Productos en favoritos:", list(favoritos_ids))

    # Guardar los IDs de los productos de la búsqueda en la sesión
    request.session['productos_busqueda'] = [producto.id for producto in productos]
    
    return render(request, 'BuscarProd.html', {
        'producto': productos,
        'categorias': categorias,
        "favoritos_ids": favoritos_ids,
        'templateB': templateB,
    })


def filtro_productos_view(request):
    # Obtener los IDs de los productos de la búsqueda almacenados en la sesión
    productos_busqueda_ids = request.session.get('productos_busqueda', None)
    
    # Obtener la lista inicial de productos con base en la búsqueda o todos si no hubo búsqueda
    if productos_busqueda_ids:

        productos = ProductoDb.objects.filter(cantidad__gt=0, id__in=productos_busqueda_ids)
    else:
        productos = ProductoDb.objects.filter(cantidad__gt=0).order_by('-visitas')
    
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
def eliminar_publicacion(request, producto_id):
    print(f"Received request to delete product ID: {producto_id}")  # Debugging
    if request.method == 'POST':  # Ensure it's a POST request
        producto = get_object_or_404(ProductoDb, id=producto_id, usuario_fk=request.user.usuariodb)
        print(f"Deleting product: {producto}")  # Debugging
        producto.delete()
        return JsonResponse({'success': True})
    print("Invalid request method.")  # Debugging
    return render(request, 'deleteProduct.html', {'usuario': request.user.usuariodb})



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

    if producto.usuario_fk == request.user.usuariodb:
        messages.error(request, "No puedes agregar tus propios productos al carrito.")
        return redirect('home', producto_id=producto_id)
    
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

    # Actualizar estados de los productos en promoción del usuario
    productos = ProductoDb.objects.filter(usuario_fk=usuario, estado='promocion')
    for producto in productos:
        producto.actualizar_estado()

    # Mostrar todos los productos del usuario
    productos = ProductoDb.objects.filter(usuario_fk=usuario)
    return render(request, "Mis_publiccaciones.html", {
        'mis_productos': productos,
        'usuario': usuario  
    })


@login_required
def editar_producto(request, producto_id):
    # Obtener el producto por ID
    producto = get_object_or_404(ProductoDb, id=producto_id)

    if request.method == 'POST':
        # Al recibir una solicitud POST, procesar el formulario con los datos actuales del producto
        form = RegistroProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            # Si el formulario es válido, guardar los cambios
            form.save()
            # Redirigir a una página de confirmación o a la lista de productos
            return redirect('confirmacion_producto')  # Asegúrate de tener esta URL configurada en tus urls.py
        else:
            # Si el formulario no es válido, puedes agregar un mensaje de error aquí (opcional)
            # Puedes mostrar mensajes de error en la plantilla
            return render(request, 'registro_producto.html', {'form': form, 'producto': producto, 'error': 'Hubo un error al guardar los cambios'})
    
    else:
        # Si la solicitud es GET, pre-llenar el formulario con los datos actuales del producto
        form = RegistroProductoForm(instance=producto)

    # Renderizar el formulario de edición con los datos actuales del producto
    return render(request, 'registro_producto.html', {'form': form, 'producto': producto})


@login_required
def delete_image(request, image_id):
    """
    View to handle deletion of an image from a product.
    """
    imagen = get_object_or_404(ImagenProductoDB, id=image_id, producto_fk__usuario_fk=request.user.usuariodb)
    imagen.delete()
    return JsonResponse({'success': True})
    

@login_required
def eliminar_producto(request, producto_id):
    print(f"Received request to delete product ID: {producto_id}")  # Debugging
    if request.method == 'POST':  # Ensure it's a POST request
        producto = get_object_or_404(ProductoDb, id=producto_id, usuario_fk=request.user.usuariodb)
        print(f"Deleting product: {producto}")  # Debugging
        producto.delete()
        return JsonResponse({'success': True})
    print("Invalid request method.")  # Debugging
    return render(request, 'deleteProduct.html', {'usuario': request.user.usuariodb})

def confirmacion_producto(request):
    return render(request, 'confirmacion_producto.html')

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
        print("Todo llego de manera correcta")
        print("Descuento es: "+ str(descuento))
        producto.descuento = descuento
        producto.estado = 'promocion'
        producto.fecha_inicio_promocion = fecha_inicio
        producto.fecha_fin_promocion = fecha_fin
        producto.save()

        messages.success(request, 'Descuento y fechas de promoción actualizados con éxito.')

        # Redirigir a "mis publicaciones"
        return redirect('mis_publicaciones')

    return render(request, 'crear_oferta.html', {'productos': productos})

@transaction.atomic
def procesar_transaccion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo')  # Compra o Venta
            producto_id = data.get('producto_id')
            cantidad = int(data.get('cantidad'))
            detalles = data.get('detalles', '')

            producto = get_object_or_404(ProductoDb, id=producto_id)

            if tipo == 'Compra' and producto.usuario_fk == request.user.usuariodb:
                return JsonResponse({'error': 'No puedes comprar tus propios productos.'}, status=400)

            if tipo == 'Compra':
                producto.ajustar_stock(cantidad, operacion='restar')
            elif tipo == 'Venta':
                producto.ajustar_stock(cantidad, operacion='sumar')

            nueva_transaccion = Transaccion.objects.create(
                tipo=tipo,
                usuario=request.user.usuariodb,
                producto=producto,
                cantidad=cantidad,
                detalles=detalles
            )
            Transaccion.objects.create(
                tipo='Venta',
                usuario=producto.usuario_fk,
                producto=producto,
                cantidad=cantidad,
                detalles=f"Venta del producto: {producto.nombre} a {request.user.usuariodb}",
            )

            return JsonResponse({
                'message': 'Transacción procesada con éxito',
                'precio_total': nueva_transaccion.precio_total
            })

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@transaction.atomic
def procesar_carrito(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para realizar una compra.")
        return redirect('Carrito')  # Redirige al carrito si no está autenticado

    try:
        # Obtiene el carrito del usuario
        carrito = CarritoDB.objects.get(usuario_fk=request.user.usuariodb)

        # Verifica que el carrito no esté vacío
        productos_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)
        if not productos_carrito.exists():
            messages.error(request, "El carrito está vacío.")
            return redirect('Carrito')  # Redirige al carrito si está vacío

        total = 0  # Acumulador para el costo total

        # Procesa cada producto en el carrito
        for item in productos_carrito:
            producto = item.producto_fk

            # Verifica stock
            if producto.cantidad < item.cantidad:
                raise ValueError(f"Stock insuficiente para el producto {producto.nombre}")

            # Ajusta stock
            producto.ajustar_stock(item.cantidad, operacion='restar')

            # Registra la transacción
            Transaccion.objects.create(
                tipo='Compra',
                usuario=request.user.usuariodb,
                producto=producto,
                cantidad=item.cantidad,
                detalles=f"Compra desde carrito: {producto.nombre}",
            )

            vendedor = producto.usuario_fk  # Usuario vendedor
            Transaccion.objects.create(
                tipo='Venta',
                usuario=vendedor,
                producto=producto,
                cantidad=item.cantidad,
                detalles=f"Venta del producto: {producto.nombre} a {request.user.username}",
            )

            total += item.calcular_subtotal()  # Acumula el subtotal

        # Vacía el carrito
        productos_carrito.delete()

        # Mensaje de éxito
        messages.success(request, f"Compra realizada con éxito. Total: Bs {total}")
        return redirect('Carrito')  # Redirige al carrito tras una compra exitosa

    except CarritoDB.DoesNotExist:
        messages.error(request, "No se encontró un carrito activo.")
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error procesando el carrito: {str(e)}")

    return redirect('Carrito')

import qrcode 
from io import BytesIO
from django.core.files.base import ContentFile

def generar_codigo_qr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue())

def confirmar_compra(request, producto_id):
    producto = get_object_or_404(ProductoDb, id=producto_id)
    direccion_envio = "Cochabamba/Cercado/Av. Villazón Km 6"  # Puedes usar datos dinámicos

    qr_image_url = generar_codigo_qr(producto)  # Lógica para generar el QR

    return render(request, 'compra.html', {
        'producto': producto,
        'direccion_envio': direccion_envio,
        'qr_image_url': qr_image_url,
    })

def proceder_pago_carrito(request):
    productos_carrito = obtener_productos_carrito(request)
    if not productos_carrito:
        return render(request, 'proceder_pago_carrito.html', {
            'error': 'El carrito está vacío',
        })

    direccion_envio = "Cochabamba/Cercado/Av. Villazón Km 6"  # Ejemplo de dirección
    qr_image_url = generar_codigo_qr_para_carrito(productos_carrito)

    total = sum(item.calcular_subtotal() for item in productos_carrito)

    return render(request, 'proceder_pago_carrito.html', {
        'productos_carrito': productos_carrito,
        'direccion_envio': direccion_envio,
        'qr_image_url': qr_image_url,
        'total': total,
    })


def ajustar_stock(self, cantidad, operacion='restar'):
    if operacion == 'restar' and self.cantidad < cantidad:
        raise ValueError("Stock insuficiente para realizar esta operación")
    elif operacion == 'sumar':
        self.cantidad += cantidad
    else:
        self.cantidad -= cantidad
    self.save()

def obtener_productos_carrito(request):
    # Verifica que el usuario esté autenticado
    if not request.user.is_authenticated:
        return None  # O maneja carritos anónimos si lo prefieres

    # Obtén el carrito activo del usuario
    carrito, creado = CarritoDB.objects.get_or_create(usuario_fk=request.user.usuariodb)

    # Obtén los productos en el carrito
    productos_carrito = CarritoProductoDB.objects.filter(carrito_fk=carrito)

    return productos_carrito

def generar_codigo_qr_para_carrito(productos_carrito):
    # Construye un texto con la información de los productos
    texto_qr = "Carrito de compras:\n"
    for item in productos_carrito:
        texto_qr += f"{item.producto_fk.nombre} - Cantidad: {item.cantidad} - Subtotal: Bs {item.calcular_subtotal()}\n"
    
    # Genera el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(texto_qr)
    qr.make(fit=True)

    # Crea una imagen del QR
    img = qr.make_image(fill='black', back_color='white')

    # Guarda la imagen en memoria para devolverla
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return qr_base64

def historial_transacciones_view(request):
    usuario = request.user.usuariodb  # Usuario autenticado
    transacciones = Transaccion.objects.filter(usuario=usuario)  # Todas las transacciones del usuario
    compras = transacciones.filter(tipo='Compra')  # Solo compras
    ventas = transacciones.filter(tipo='Venta')  # Solo ventas

    context = {
        'transacciones': transacciones,
        'compras': compras,
        'ventas' : ventas
    }
    return render(request, 'Historial.html', context)


from django.contrib import messages

def solicitar_cotizacion(request, producto_id=None):
    # Obtener o inicializar el carrito
    carrito = request.session.get('carrito', [])

    # Si se proporciona un producto_id, agregar al carrito solo si no está presente
    if producto_id and not any(item['id'] == producto_id for item in carrito):
        producto = get_object_or_404(ProductoDb, id=producto_id)
        carrito.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'cantidad': 1,
        })
        request.session['carrito'] = carrito
        # Redirigir sin argumento producto_id para evitar bucles
        return redirect('solicitar_cotizacion', producto_id=0)

    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            # Procesar datos del formulario
            nombre = form.cleaned_data['nombre_completo']
            correo = form.cleaned_data['correo_electronico']
            telefono = form.cleaned_data['numero_telefono']
            comentarios = form.cleaned_data.get('comentarios', 'N/A')

            # Detalles de los productos
            productos = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')

            # Generar mensaje para el correo
            detalles_productos = "\n".join(
                f"- {prod} (Cantidad: {cant})"
                for prod, cant in zip(productos, cantidades)
            )
            mensaje = f"""
            Nueva solicitud de cotización:
            Nombre: {nombre}
            Correo: {correo}
            Teléfono: {telefono}
            Productos:\n{detalles_productos}
            Comentarios: {comentarios}
            """

            # Enviar correo
            send_mail(
                subject="Solicitud de Cotización",
                message=mensaje,
                from_email='tienda@ejemplo.com',
                recipient_list=[correo],
            )

            # Limpiar el carrito
            

            # Agregar mensaje de confirmación al contexto
            messages.success(request, 'Gracias por su solicitud. Le enviaremos la cotización a su correo.')
            request.session['carrito'] = []
            #return redirect('solicitar_cotizacion')  # Redirigir para limpiar formulario y mostrar mensaje

    else:
        form = CotizacionForm()

    # Renderizar la página inicial con el formulario y el carrito
    return render(request, 'cotizacion.html', {'form': form, 'carrito': carrito})


def eliminar_todo_el_carrito(request, product_index=None):
    carrito = request.session.get('carrito', [])
    
    # Eliminar producto específico
    if product_index is not None:
        carrito.pop(product_index, None)

    # Limpiar carrito si no hay índice
    else:
        carrito = []

    request.session['carrito'] = carrito
    return JsonResponse({'mensaje': 'Carrito actualizado', 'carrito': carrito})