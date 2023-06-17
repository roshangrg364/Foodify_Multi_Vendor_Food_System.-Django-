from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User, UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_customer
from accounts.forms import UserProfileForm, UserForm, UserFormForCustomer
from django.contrib import messages
from orders.models import Order, OrderItem
import simplejson as json


# Create your views here.
@login_required(login_url="login")
@user_passes_test(check_customer)
def customerprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserFormForCustomer(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("customer_profile")
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserFormForCustomer(instance=request.user)
    data = {
        "profile_form": profile_form,
        "user_form": user_form,
        "profile": profile,
    }
    return render(request, "customer/customer_profile.html", data)


def myorders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    data = {"orders": orders}
    return render(request, "customer/my_orders.html", data)


def orderdetails(request, order_id):
    order = Order.objects.get(pk=order_id)
    if not order:
        messages.error(request, "order not found")
        return redirect("customer")
    order_items = OrderItem.objects.filter(order=order)
    sub_total = 0
    for item in order_items:
        sub_total += item.price * item.quantity
    tax_data = json.loads(order.tax_data)
    data = {
        "order": order,
        "order_items": order_items,
        "sub_total": sub_total,
        "tax_data": tax_data,
    }
    return render(request, "customer/order_detail.html", data)
