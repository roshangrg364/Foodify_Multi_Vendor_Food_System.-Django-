from django.contrib import admin
from .models import Category, Menu

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ("category_name",)}
    list_display = (
        "category_name",
        "vendor",
        "created_on",
        "updated_at",
    )
    search_fields = (
        "category_name",
        "vendor__vendor_name",
    )


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("menu_title",)}
    list_display = (
        "menu_title",
        "category",
        "vendor",
        "price",
        "is_available",
        "updated_at",
    )
    search_fields = (
        "menu_title",
        "category__category_name",
        "price",
    )
    list_filter = ("is_available",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Menu, FoodItemAdmin)
