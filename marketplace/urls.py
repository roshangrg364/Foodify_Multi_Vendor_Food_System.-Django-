from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:vendor_slug>", views.vendordetail, name="vendor_detail"),
    # addtocart
    path("add_to_cart/<int:menu_id>/", views.addtocart, name="add_to_cart"),
    # decreascartitem
    path(
        "remove_from_cart/<int:menu_id>/",
        views.removefromcart,
        name="remover_from-cart",
    ),
    # delete_cart_item
    path(
        "delete_cart_item/<int:cart_id>/",
        views.deletecartitem,
        name="delete_cart_item",
    ),
]
