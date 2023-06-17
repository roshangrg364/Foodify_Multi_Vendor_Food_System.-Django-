from django.shortcuts import render, redirect, get_object_or_404
from marketplace.models import Cart
from marketplace.context_processor import getCartAmount
from .forms import OrderForm
from .models import Order, Payment, OrderItem
import simplejson as json
from .utils import generateOrder_number
from django.http import JsonResponse
import uuid
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.


@login_required(login_url="login")
def placeorder(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.count() <= 0:
        return redirect("marketplace")

    cart_amounts = getCartAmount(request)
    subtotal = cart_amounts["subtotal"]
    total_tax = cart_amounts["tax"]
    grand_total = cart_amounts["total"]
    tax_details = cart_amounts["tax_details"]
    try:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                existing_order = Order.objects.filter(
                    user=request.user, status=Order.Status_New
                ).first()
                if existing_order:
                    existing_order.delete()
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                phone = form.cleaned_data["phone"]
                email = form.cleaned_data["email"]
                address = form.cleaned_data["address"]
                country = form.cleaned_data["country"]
                state = form.cleaned_data["state"]
                city = form.cleaned_data["city"]
                pin_code = form.cleaned_data["pin_code"]
                payment_method = request.POST["payment_method"]

                order = Order()
                order.first_name = first_name
                order.last_name = last_name
                order.phone = phone
                order.email = email
                order.address = address
                order.country = country
                order.state = state
                order.city = city
                order.pin_code = pin_code
                order.user = request.user
                order.total = grand_total
                order.total_tax = total_tax
                order.payment_method = payment_method
                order.status = Order.Status_New
                order.tax_data = json.dumps(tax_details)
                order.save()
                order.order_number = generateOrder_number(order.id)
                order.save()
                data = {"order": order, "cart_items": cart_items}

                return render(request, "orders/place_order.html", data)
            else:
                print(form.errors)
                carts = Cart.objects.filter(user=request.user).order_by("created_on")
                data = {"order_form": form, "cart_items": carts}
                return render(request, "marketplace/checkout.html", data)
    except Exception as error:
        print(error)
        return redirect("checkout")


def orderpayment(request):
    if request.user.is_authenticated:
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            try:
                with transaction.atomic():
                    if request.method == "POST":
                        order_number = request.POST["order_number"]
                        payment_method = request.POST["payment_method"]
                        transaction_id = request.POST["transaction_id"]
                        order = Order.objects.get(
                            user=request.user, order_number=order_number
                        )
                        if order.payment_method != payment_method:
                            raise Exception("Invalid Payment Method")
                        if not transaction_id:
                            transaction_id = uuid.uuid1()
                        payment_status = Payment.Status_Pending
                        if order.payment_method == Payment.PaymentMethod_Paypal:
                            payment_status = Payment.Status_Completed
                        # save payment
                        payment = Payment(
                            user=request.user,
                            transaction_id=transaction_id,
                            payment_method=payment_method,
                            amount=order.total,
                            status=payment_status,
                        )
                        payment.save()
                        # update order
                        order.payment = payment
                        order.is_ordered = True
                        order.status = Order.Status_Accepted
                        order.save()

                        # add orderitem
                        cart_items = Cart.objects.filter(user=request.user)
                        for item in cart_items:
                            order_item = OrderItem(
                                order=order,
                                payment=payment,
                                user=request.user,
                                menu=item.menu,
                                quantity=item.quantity,
                                price=item.menu.price,
                                amount=(item.menu.price * item.quantity),
                            )
                            order_item.save()

                        # send notification to customer
                        mail_subject = "Thank you for ordering."
                        mail_template = "orders/order_confirmation_email.html"
                        to_email = order.email
                        data = {"order": order, "user": request.user}
                        send_notification(mail_subject, mail_template, data, to_email)

                        # send notification to vendor
                        vendors = []
                        for cart in cart_items:
                            vendor_id = cart.menu.vendor.id
                            vendor_email = cart.menu.vendor.user.email

                            if vendor_id not in vendors:
                                vendors.append(vendor_id)
                                mail_subject = "You have received a new order."
                                mail_template = "orders/order_received_email.html"
                                items = cart_items.filter(menu__vendor__id=vendor_id)
                                data = {
                                    "order": order,
                                    "user": request.user,
                                    "cart_items": items,
                                    "vendor": item.menu.vendor,
                                }
                                send_notification(
                                    mail_subject, mail_template, data, vendor_email
                                )
                                # delete cart items
                                cart_items.delete()

                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "Ordered Successfully",
                                "order_id": order.id,
                                "transaction_id": order.payment.transaction_id,
                            }
                        )
            except Exception as error:
                transaction.rollback()
                return JsonResponse({"status": "failed", "message": error})
    else:
        return JsonResponse(
            {"status": "unauthenticated", "message": "user unathenticated"}
        )


def orderconfirmation(request):
    order_id = request.GET.get("order_id")
    transaction_id = request.GET.get("transaction_id")
    try:
        order = Order.objects.get(
            id=order_id,
            payment__transaction_id=transaction_id,
            is_ordered=True,
        )
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
        return render(request, "orders/order_confirmed.html", data)
    except Exception as error:
        print(error)
        return redirect("home")
