from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistema.views import IndexView, ProductoView, BuscarView

urlpatterns = [
    path('', IndexView, name='index'),  # Asegúrate de usar as_view() si es una vista basada en clase
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
    path('buscar/', BuscarView, name='buscar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
