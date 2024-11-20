from sistema.models import UsuarioDB, CarritoProductoDB
from django.db.models import Sum

def cart_count(request):
    if request.user.is_authenticated:  # Only fetch the cart count for logged-in users
        try:
            # Retrieve the logged-in user's cart count from the database
            usuario = request.user.usuariodb
            cart_count = CarritoProductoDB.objects.filter(carrito_fk__usuario_fk=usuario).aggregate(
                total_quantity=Sum('cantidad')
            )['total_quantity'] or 0
        except UsuarioDB.DoesNotExist:
            # If the user does not have a UsuarioDB profile, default to 0
            cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}

def user_profile(request):
    if request.user.is_authenticated:
        return {"usuario": request.user.usuariodb}
    return {}