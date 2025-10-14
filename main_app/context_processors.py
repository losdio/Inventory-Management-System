from .models import Cart

def cart_context(request):
    context = {}
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user_id=request.user)
        context['cart_id'] = user_cart.id if user_cart else None
    return context