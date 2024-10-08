from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistema.views import IndexView, ProductoView, BuscarView, CheckoutView

urlpatterns = [
    path('', IndexView, name='index'),
    
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
    
    path('layout/',CheckoutView,name='layout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)