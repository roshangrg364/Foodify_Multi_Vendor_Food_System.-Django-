from .models import Cart
from menu.models import Menu
from django.db.models import Count


def getCounter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = (
                Cart.objects.filter(user=request.user)
                .values("menu")
                .annotate(count=Count("id"))
            )
            cart_count = len(cart_items)
        except:
            cart_count = 0

    return dict(cart_count=cart_count)


def getCartAmount(request):
    subtotal = 0
    tax = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += item.menu.price * item.quantity

        total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, total=total)
