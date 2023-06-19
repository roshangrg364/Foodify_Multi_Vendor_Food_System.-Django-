from django.contrib import admin
from .models import Order, OrderItem, Payment


# Register your model
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = (
        "order",
        "payment",
        "menu",
        "quantity",
        "price",
        "amount",
        "user",
    )
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "name",
        "email",
        "phone",
        "total",
        "payment_method",
        "status",
        "vendors_list",
        "is_ordered",
    ]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
