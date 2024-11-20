from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),  # Ruta principal para index.html
    path('producto/<int:id>/', views.producto_view, name='detalle_producto'),
    path('buscar/', views.buscar_view, name='buscar'),
    path('carrito/', views.carrito_view, name='Carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_a_carrito'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('check_email/', views.check_email, name='check_email'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('success/', views.success, name='success'),
    path('terms-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('ajax/cargar-provincias/', views.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-municipios/', views.cargar_municipios, name='ajax_cargar_municipios'),
    path('test/', views.test, name='testeo'),
    path('home/', views.home_view, name='home'),
    path('perfil/', views.perfil_view, name='profile'),
    path('registro-producto/', views.registro_producto, name='registro_producto'),
    path('vender/', views.vender_view, name='vender'),
    path('lista-favoritos/', views.ver_lista_favoritos, name='listaFavoritos'),
    path('lista-favoritos/agregar/<int:producto_id>/', views.agregar_a_lista_favoritos, name='agregarFavorito'),
    path('lista-favoritos/eliminar/<int:producto_id>/', views.eliminar_de_lista_favoritos, name='eliminarFavorito'),
    path('filtro-productos/', views.filtro_productos_view, name='filtro_productos'),
    path('profile/photo-update/', views.update_profile_photo, name='profile_photo_update'),
    path('confirmacion-producto/', views.confirmacion_producto, name='confirmacion_producto'),
    path('api/publicaciones/', views.PublicacionesUsuarioAPIView.as_view(), name='publicaciones_usuario'),
    path('api/publicaciones/<int:id>/', views.ActualizarPublicacionAPIView.as_view(), name='actualizar_publicacion'),
    path('productos/', views.product_list, name='product_list'),




    path('transacciones/', views.transacciones_view, name='transacciones'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





























