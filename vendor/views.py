from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.forms import UserProfileForm
from .forms import VendorForm
from .models import vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor

# Create your views here.


@login_required(login_url="login")
@user_passes_test(check_vendor)
def vendorprofile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor_data = get_object_or_404(vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor_data)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("vendorprofile")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=user_profile)
        vendor_form = VendorForm(instance=vendor_data)

    data = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": user_profile,
        "vendor": vendor_data,
    }
    return render(request, "vendor/vendorprofile.html", data)
