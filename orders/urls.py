from django.urls import path
from . import views

urlpatterns = [
    path("placeorder", views.placeorder, name="place_order"),
    path("order-payment/", views.orderpayment, name="order_payment"),
    path("order-confirmation/", views.orderconfirmation, name="order_confirmation"),
]
