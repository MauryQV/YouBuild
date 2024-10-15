def cart_count(request):
    cart_count = request.session.get('cart_count', 0)
    return {'cart_count': cart_count}