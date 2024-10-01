from django.urls import path
from sistema.views import IndexView, ProductoView



urlpatterns = [
    path('',IndexView),
    path('producto/<int:id>/', ProductoView, name='detalle_producto'),
]
