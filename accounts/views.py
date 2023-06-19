from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from .utils import getdashboardurl, send_verification_email
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from orders.models import Order, OrderItem
from django.db.models import Sum
import datetime


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

            # send verification email
            email_subject = "Email Verification"
            template_path = "accounts/emails/AccountVerificationEmail.html"
            send_verification_email(request, user, email_subject, template_path)

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
            vendor_name = vendor_form.cleaned_data["vendor_name"]
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.slug = slugify(vendor_name) + str(user.id)
            messages.success(request, "Restaurant Registered Successfully")
            vendor.save()

            # send verification mail
            email_subject = "Email Verification"
            template_path = "accounts/emails/AccountVerificationEmail.html"
            send_verification_email(request, user, email_subject, template_path)

            return redirect("registervendor")
        else:
            print(form.errors)
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
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "created_at"
    )
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(created_at__month=current_month)
    current_month_amount = 0
    for order in current_month_orders:
        current_month_amount += order.total

    total_order_amount = orders.aggregate(Sum("total"))
    total_orders = orders.count()
    data = {
        "orders": orders[:5],
        "total_order_amount": total_order_amount["total__sum"],
        "order_count": total_orders,
        "current_month_amount": current_month_amount,
    }
    return render(request, "accounts/customerdashboard.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def vendordashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by(
        "-created_at"
    )
    # current month revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(created_at__month=current_month)
    current_month_revenue = 0
    for order in current_month_orders:
        current_month_revenue += order.get_total_by_vendor()["grand_total"]

    # total revenue
    total_revenue = 0
    for order in orders:
        total_revenue += order.get_total_by_vendor()["grand_total"]
    data = {
        "orders": orders[:5],
        "order_count": orders.count(),
        "total_revenue": total_revenue,
        "current_month_revenue": current_month_revenue,
    }
    return render(request, "accounts/vendordashboard.html", data)


def activate(request, uidb64, token):
    try:
        decoded_uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=decoded_uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "congratulations your account has been activated succesfully"
        )
        return redirect("myaccount")

    else:
        messages.error(request, "Invalid activation link")
        return redirect("home")


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset password link
            email_subject = "Reset Password"
            template_path = "accounts/emails/ResetPasswordLink.html"
            send_verification_email(request, user, email_subject, template_path)
            messages.success(
                request, "Password reset link has been sent to your email successfully."
            )
            return redirect("login")
        else:
            messages.error("Account does not exists")
            return redirect("forgot_password")
    return render(request, "accounts/ForgotPassword.html")


def validateresetpassword(request, uidb64, token):
    try:
        decoded_uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=decoded_uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = decoded_uid
        messages.success(request, "Please  reset password")
        return redirect("reset_password")

    else:
        messages.error(request, "Invalid reset password link or expired link")
        return redirect("forgot_password")


def resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            user_id = request.session.get("uid")
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfull")
            return redirect("login")
        else:
            messages.error(request, "password do not match")
            return redirect("reset_password")

    return render(request, "accounts/ResetPassword.html")
