from django.urls import path
from . import views
from accounts import views as AccountView

urlpatterns = [
    path("", AccountView.vendordashboard),
    path("profile/", views.vendorprofile, name="vendorprofile"),
]
