from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User, UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_customer
from accounts.forms import UserProfileForm, UserForm, UserFormForCustomer
from django.contrib import messages
from orders.models import Order, OrderItem
import simplejson as json
from django.db.models import Q
from django.db import transaction


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


@login_required(login_url="login")
@user_passes_test(check_customer)
def myorders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    data = {"orders": orders}
    return render(request, "customer/my_orders.html", data)


@login_required(login_url="login")
@user_passes_test(check_customer)
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


@login_required(login_url="login")
@user_passes_test(check_customer)
def pendingorders(request):
    pending_orders = Order.objects.filter(
        user=request.user,
        is_ordered=True,
    ).exclude(Q(status=Order.Status_Cancelled) | Q(status=Order.Status_Completed))

    data = {"orders": pending_orders}
    return render(request, "customer/pending_customer_orders.html", data)


@login_required(login_url="login")
@user_passes_test(check_customer)
def cancelorder(request, order_id):
    order = Order.objects.filter(id=order_id, is_ordered=True).first()
    if not order:
        messages.info(request, "Order not found")
        return redirect("customer_pending_orders")
    if order.status == Order.Status_Completed:
        messages.info(request, "Order already completed")
        return redirect("customer_pending_orders")
    if order.status == Order.Status_Cancelled:
        messages.info(request, "Order already Cancelled")
        return redirect("customer_pending_orders")

    order_items = OrderItem.objects.filter(order=order).exclude(
        Q(status=OrderItem.Status_Completed) | Q(status=OrderItem.Status_Cancelled)
    )

    processingOrderitems = order_items.filter(status=OrderItem.Status_Process)
    if processingOrderitems.count() > 0:
        messages.info(request, "Order processing have already started")
        return redirect("customer_pending_orders")

    with transaction.atomic():
        order.status = Order.Status_Cancelled
        order.save()
        for item in processingOrderitems:
            item.status = OrderItem.Status_Cancelled
            item.save()

    messages.info(request, "Order Cancelled Successfully")
    return redirect("customer_pending_orders")
