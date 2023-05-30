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
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotpassword/", views.forgotpassword, name="forgot_password"),
    path(
        "validateresetpassword/<uidb64>/<token>/",
        views.validateresetpassword,
        name="validate_reset_password",
    ),
    path("resetpassword/", views.resetpassword, name="reset_password"),
]
