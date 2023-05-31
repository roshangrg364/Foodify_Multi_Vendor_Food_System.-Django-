from vendor.models import vendor


def get_vendor(request):
    try:
        Vendor = vendor.objects.get(user=request.user)
    except:
        Vendor = None

    data = {
        "vendor": Vendor,
    }
    return data
