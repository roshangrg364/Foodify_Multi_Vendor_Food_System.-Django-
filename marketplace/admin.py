from django.contrib import admin
from .models import Cart

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "menu", "quantity", "created_on", "modified_on")


admin.site.register(Cart, CartAdmin)
