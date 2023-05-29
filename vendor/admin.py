from django.contrib import admin
from .models import vendor


# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_name", "is_approved", "created_on", "modified_on")


admin.site.register(vendor, VendorAdmin)
