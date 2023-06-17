from vendor.models import Vendor
from accounts.models import UserProfile
from django.conf import settings


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None

    data = {
        "vendor": vendor,
    }
    return data


def get_userprofile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None

    data = {
        "user_profile": user_profile,
    }
    return data


def get_paypal_client_id(request):
    return {"PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID}
