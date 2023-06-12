from . import views
from django.urls import path
from accounts import views as Accountviews

urlpatterns = [
    path("", Accountviews.customerdashboard, name="customer"),
    path("profile/", views.customerprofile, name="customer_profile"),
]
