from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
<<<<<<< HEAD
from .views import registrar_usuario, CustomLoginView, index_view, producto_view, buscar_view, carrito_view, eliminar_producto, update_cart_quantity, agregar_al_carrito, get_cart_count, test, home_view, perfil_view, registro_producto, custom_logout_view, cargar_provincias, cargar_municipios
from .views import gestionar_usuario_view  # Asegúrate de importar tu vista
=======
from .views import *
>>>>>>> origin/develop

urlpatterns = [
    path('', index_view, name='index'),
    path('producto/<int:id>/', producto_view, name='detalle_producto'),
    path('buscar/', buscar_view, name='buscar'),
    path('carrito/', carrito_view, name='Carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_a_carrito'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('registro/', registrar_usuario, name='registro'),
    path('success/', views.success, name='success'), 
    path('terms-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('ajax/cargar-provincias/', cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-municipios/', cargar_municipios, name='ajax_cargar_municipios'),
    path('test/', test, name='testeo'),
    path('home/', home_view, name='home'),
    path('perfil/', perfil_view, name='profile'),
        path('gestionar-usuario/', gestionar_usuario_view, name='gestionar_usuario'),

    path('registro-producto/', registro_producto, name='registro_producto'),
    path('vender/', vender_view, name='vender'),
    
   path('lista-favoritos/', ver_lista_favoritos, name='listaFavoritos'),
    path('lista-favoritos/agregar/<int:producto_id>/', agregar_a_lista_favoritos, name='agregarFavorito'),
    path('lista-favoritos/eliminar/<int:producto_id>/', eliminar_de_lista_favoritos, name='eliminarFavorito'),
    path('filtro-productos/', filtro_productos_view, name='filtro_productos'),
    path('profile/photo-update/', update_profile_photo, name='profile_photo_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

