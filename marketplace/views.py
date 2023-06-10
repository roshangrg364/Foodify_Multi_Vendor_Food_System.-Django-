from django.shortcuts import render, get_object_or_404, HttpResponse
from vendor.models import Vendor, OpeningHour
from menu.models import Category, Menu
from marketplace.models import Cart
from django.db.models import Prefetch
from django.http import JsonResponse
from .context_processor import getCounter, getCartAmount
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, time, datetime

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    data = {
        "vendors": vendors,
        "vendor_count": vendor_count,
    }
    return render(request, "marketplace/listings.html", data)


def vendordetail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch("menus", queryset=Menu.objects.filter(is_available=True))
    )
    cart_items = None
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by(
        "day", "-from_hour"
    )

    # check current day opening_hour
    today = date.today().isoweekday()
    current_opening_hour = OpeningHour.objects.filter(vendor=vendor, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    data = {
        "vendor": vendor,
        "categories": categories,
        "cart_items": cart_items,
        "opening_hours": opening_hours,
        "current_opening_hours": current_opening_hour,
    }
    return render(request, "marketplace/vendor_detail.html", data)


def addtocart(request, menu_id):
    if request.user.is_authenticated:
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            try:
                menu = Menu.objects.filter(id=menu_id).first()
                if menu is None:
                    raise Exception("Menu does not exist")
                userCartData = Cart.objects.filter(user=request.user, menu=menu).first()
                if userCartData is not None:
                    userCartData.quantity += 1
                    userCartData.save()
                else:
                    userCartData = Cart.objects.create(
                        user=request.user, menu=menu, quantity=1
                    )
                    userCartData.save()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "item added sucessfully",
                        "cart_counter": getCounter(request),
                        "quantity": userCartData.quantity,
                        "cart_amount": getCartAmount(request),
                    }
                )
            except:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "something went wrong. please contact to administrator",
                    }
                )
        else:
            return JsonResponse({"status": "error", "message": "request is invalid"})
    else:
        return JsonResponse(
            {"status": "unauthenticated", "message": "please login to continue"}
        )


def removefromcart(request, menu_id):
    if request.user.is_authenticated:
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            try:
                menu = Menu.objects.filter(id=menu_id).first()
                if menu is None:
                    raise Exception("Menu does not exist")
                userCartData = Cart.objects.filter(user=request.user, menu=menu).first()
                menu_quantity = 0
                if userCartData is not None:
                    if userCartData.quantity == 1:
                        userCartData.delete()
                    else:
                        userCartData.quantity -= 1
                        userCartData.save()
                        menu_quantity = userCartData.quantity
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "item decreased sucessfully",
                        "cart_counter": getCounter(request),
                        "quantity": menu_quantity,
                        "cart_amount": getCartAmount(request),
                    }
                )
            except:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "something went wrong. please contact to administrator",
                    }
                )
        else:
            return JsonResponse({"status": "error", "message": "request is invalid"})
    else:
        return JsonResponse(
            {"status": "unauthenticated", "message": "please login to continue"}
        )


def deletecartitem(request, cart_id):
    if request.user.is_authenticated:
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            try:
                userCartData = Cart.objects.filter(
                    user=request.user, id=cart_id
                ).first()
                if userCartData is not None:
                    userCartData.delete()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "item deleted sucessfully",
                        "cart_counter": getCounter(request),
                        "cart_amount": getCartAmount(request),
                    }
                )
            except:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "something went wrong. please contact to administrator",
                    }
                )
        else:
            return JsonResponse({"status": "error", "message": "request is invalid"})
    else:
        return JsonResponse(
            {"status": "unauthenticated", "message": "please login to continue"}
        )


@login_required(login_url="login")
def cartdetail(request):
    carts = Cart.objects.filter(user=request.user).order_by("created_on")
    data = {"cart_items": carts}
    return render(request, "marketplace/cartdetail.html", data)


def search(request):
    address = request.GET["address"]
    name = request.GET["restaurantname"]
    radius = request.GET["radius"]
    lat = request.GET["latitude"]
    longitude = request.GET["longitude"]
    vendors = None
    vendor_count = 0
    vendors = Vendor.objects.filter(user__is_active=True, is_approved=True)
    if name:
        if name:
            vendors_with_given_menu = Menu.objects.filter(
                is_available=True, menu_title__icontains=name
            ).values_list("vendor", flat=True)

            vendors = vendors.filter(
                Q(id__in=vendors_with_given_menu) | Q(vendor_name__icontains=name)
            )

    if address:
        vendors = vendors.filter(user_profile__address__icontains=address)
    vendor_count = vendors.count()
    data = {"vendors": vendors, "vendor_count": vendor_count}
    return render(request, "marketplace/listings.html", data)
