from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import registrar_usuario, CustomLoginView
from django.contrib.auth.decorators import login_required
from . import views
from sistema.views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
    #path('check/', CheckoutView, name='checkout'),  # Cambié 'layout' por 'checkout'
    path('carrito/', carrito_view, name='Carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_a_carrito'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('success/', views.success, name='success'),


    # Agrega la línea siguiente para crear la cuenta
    #path('crear-cuenta/', CrearCuentaView, name='crear_cuenta'),  # <-- Aquí

    path('registro/', registrar_usuario, name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('logout/', custom_logout_view, name='logout'),
    path('ajax/cargar-provincias/', cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-municipios/', cargar_municipios, name='ajax_cargar_municipios'),
    # path('api/registro/', RegistroUsuario.as_view(), name='registro_usuario'),

    path('test/', test, name='testeo'),
    path('home/', home_view, name='home'),
    path('perfil/', perfil_view, name='profile'),
    # Asegúrate de que esta línea esté aquí solo una vez
    
    #urls usadas para registrar producto
    path('registrar-producto/', registrar_producto, name='registrar_producto'),
    path('subcategorias/<int:categoria_id>/', cargar_subcategorias, name='obtener_subcategorias'),
    path('provincias/<int:departamento_id>/', obtener_provincias, name='obtener_provincias'),
    path('municipios/<int:provincia_id>/', obtener_municipios, name='obtener_municipios'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
