from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistema.views import IndexView, ProductoView, BuscarView, CheckoutView, carrito_view, eliminar_producto,update_cart_quantity, agregar_al_carrito, confirmacion_view, get_cart_count

urlpatterns = [
    path('', IndexView, name='index'),
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
    path('check/', CheckoutView, name='checkout'),  # Cambié 'layout' por 'checkout'
    path('carrito/', carrito_view, name='Carrito'),
    path('confirmacion/', confirmacion_view, name='confirmacion'),
    path('carrito/eliminar/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_a_carrito'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
