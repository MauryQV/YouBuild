from django.shortcuts import render,get_object_or_404
from .models import ProductoDb,CategoriaDb
#from django.http import HttpResponse
# Create your views here.

def IndexView(request):
    
    objeto = ProductoDb.objects.all().order_by("id")
    
    return render(request,"index.html",{"objeto":objeto})


def ProductoView(request,id):
    producto = get_object_or_404(ProductoDb,id=id)
    return render(request,"productos.html",{"producto":producto})
