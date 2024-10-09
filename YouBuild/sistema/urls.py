from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistema.views import IndexView, ProductoView, BuscarView, CheckoutView,carrito_view,eliminar_producto

urlpatterns = [
    path('', IndexView, name='index'),
    
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
    
    path('check/',CheckoutView,name='layout'),
    path('carrito/', carrito_view, name='Carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
