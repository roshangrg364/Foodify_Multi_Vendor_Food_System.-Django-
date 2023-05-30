from django.urls import path
from . import views


urlpatterns = [
    path("registeruser/", views.registeruser, name="registeruser"),
    path("registervendor/", views.registervendor, name="registervendor"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("customrdashboard", views.customerdashboard, name="customerdashboard"),
    path("vendordashboard", views.vendordashboard, name="vendordashboard"),
]
