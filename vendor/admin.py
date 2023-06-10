from django.contrib import admin
from .models import Vendor, OpeningHour


# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_name", "is_approved", "created_on", "modified_on")


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = (
        "vendor",
        "day",
        "from_hour",
        "to_hour",
        "is_closed",
    )


admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)
