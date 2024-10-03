from django.shortcuts import render, get_object_or_404
from .models import ProductoDb, CategoriaDb

# Vista principal
def IndexView(request):
    productos = ProductoDb.objects.all().order_by("id")  
    return render(request, "index.html", {"productos": productos}) 

def ProductoView(request, id):
    producto = get_object_or_404(ProductoDb, id=id)
    return render(request, "productos.html", {"producto": producto})
