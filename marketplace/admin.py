from django.contrib import admin
from .models import Cart, Tax

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "menu", "quantity", "created_on", "modified_on")


class TaxAdmin(admin.ModelAdmin):
    list_display = ("tax_type", "tax_percentage", "is_active")


admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
