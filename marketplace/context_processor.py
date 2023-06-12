from .models import Cart, Tax
from menu.models import Menu
from django.db.models import Count
from decimal import Decimal


def getCounter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user).values("menu")
            cart_count = len(cart_items)
        except:
            cart_count = 0

    return dict(cart_count=cart_count)


def getCartAmount(request):
    subtotal = 0
    total_tax = 0
    total = 0
    tax_details = []
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += item.menu.price * item.quantity

        taxes = Tax.objects.filter(is_active=True)

        for tax in taxes:
            tax_type = tax.tax_type
            tax_percentage = tax.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
            total_tax += tax_amount
            tax_detail = {
                "tax_type": tax_type,
                "tax_percentage": tax_percentage,
                "tax_amount": tax_amount,
            }
            tax_details.append(tax_detail)
        total = subtotal + total_tax
    return dict(subtotal=subtotal, tax=total_tax, total=total, tax_details=tax_details)
