from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistema.views import IndexView, ProductoView, BuscarView, añadir_al_carrito, ver_carrito, agregar_cantidad, eliminar_producto

urlpatterns = [
    path('', IndexView, name='index'),
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
    path('añadir_al_carrito/<int:id>/', añadir_al_carrito, name='añadir_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('agregar_cantidad/<int:producto_id>/', agregar_cantidad, name='agregar_cantidad'),  # Nueva ruta para agregar cantidad
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),  # Nueva ruta para eliminar producto
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)