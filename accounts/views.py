from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import getdashboardurl
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Create your views here.
def check_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied()


def check_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied()


def registeruser(request):
    if request.user.is_authenticated:
        messages.info(request, "user already logged in")
        return redirect("myaccount")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.role = User.CUSTOMER
            messages.success(request, "User Registered Successfully")
            user.save()
            return redirect("registeruser")
    else:
        form = UserForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/RegisterUser.html", context)


def registervendor(request):
    if request.user.is_authenticated:
        messages.info(request, "user already logged in")
        return redirect("myaccount")
    if request.method == "POST":
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            messages.success(request, "Restaurant Registered Successfully")
            vendor.save()
            return redirect("registervendor")
    else:
        form = UserForm()
        vendor_form = VendorForm()
    context = {
        "form": form,
        "vendor_form": vendor_form,
    }
    return render(request, "accounts/RegisterVendor.html", context)


def login(request):
    if request.user.is_authenticated:
        messages.info(request, "user already logged in")
        return redirect("myaccount")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("myaccount")
        else:
            messages.error(request, "Invalid email/password")
            return redirect("login")
    return render(request, "accounts/Login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("login")


@login_required(login_url="login")
def myaccount(request):
    user = request.user
    dashboardurl = getdashboardurl(user)
    return redirect(dashboardurl)


@login_required(login_url="login")
@user_passes_test(check_customer)
def customerdashboard(request):
    return render(request, "accounts/customerdashboard.html")


@login_required(login_url="login")
@user_passes_test(check_vendor)
def vendordashboard(request):
    return render(request, "accounts/vendordashboard.html")
