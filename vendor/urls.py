from django.urls import path, include
from . import views
from accounts import views as AccountView

urlpatterns = [
    path("", AccountView.vendordashboard),
    path("profile/", views.vendorprofile, name="vendorprofile"),
    path("category/", views.menu, name="category"),
    path(
        "category/menus/<int:pk>/",
        views.menusbycategory,
        name="menus_by_category",
    ),
    # Category crud
    path("category/add", views.addcategory, name="add_category"),
    path("category/update/<int:pk>/", views.editcategory, name="edit_category"),
    path("category/delete/<int:pk>/", views.deltecategory, name="delete_category"),
]
