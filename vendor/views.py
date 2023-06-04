from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.forms import UserProfileForm
from .forms import VendorForm
from .models import Vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor
from menu.models import Category, Menu
from menu.forms import CategoryForm, MenuForm
from django.template.defaultfilters import slugify

# Create your views here.


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url="login")
@user_passes_test(check_vendor)
def vendorprofile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor_data = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor_data)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("vendorprofile")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=user_profile)
        vendor_form = VendorForm(instance=vendor_data)

    data = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": user_profile,
        "vendor": vendor_data,
    }
    return render(request, "vendor/vendorprofile.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def menu(request):
    vendor_data = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor_data)
    data = {
        "categories": categories,
    }
    return render(request, "vendor/Category.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def menusbycategory(request, pk=None):
    vendor_data = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    menus = Menu.objects.filter(category=category, vendor=vendor_data)
    data = {"menus": menus, "category": category}
    return render(request, "vendor/Menu.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def addcategory(request):
    try:
        if request.method == "POST":
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                vendor = get_vendor(request)
                category_name = category_form.cleaned_data["category_name"]
                print(vendor.vendor_name)
                category = Category.objects.filter(
                    category_name__iexact=category_name, vendor=vendor
                )
                if len(category) > 0:
                    raise Exception("Category: " + category_name + " already exists.")
                category = category_form.save(commit=False)
                category.vendor = vendor
                category.category_slug = slugify(category_name) + str(vendor.pk)
                category.save()
                messages.success(request, "Category added successfully")
                return redirect("category")
            else:
                print(category_form.errors)
        else:
            category_form = CategoryForm()
        data = {"category_form": category_form}
    except Exception as error:
        category_form = CategoryForm(request.POST)
        data = {"category_form": category_form}
        messages.error(request, error)
    return render(request, "vendor/add_category.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def editcategory(request, pk=None):
    try:
        category = get_object_or_404(Category, pk=pk)
        if request.method == "POST":
            category_form = CategoryForm(request.POST, instance=category)
            if category_form.is_valid():
                vendor = get_vendor(request)
                category_name = category_form.cleaned_data["category_name"]
                category_with_same_name = Category.objects.filter(
                    category_name__exact=category_name, vendor=vendor
                )
                if category is not None and category_form != category_with_same_name:
                    raise Exception("Category: " + category_name + " already exists.")

                category = category_form.save(commit=False)
                vendor = get_vendor(request)
                category.vendor = vendor
                category.category_slug = slugify(category_name) + str(vendor.pk)
                category.save()
                messages.success(request, "Category Updated successfully")
                return redirect("category")
            else:
                print(category_form.errors)
        else:
            category_form = CategoryForm(instance=category)

        data = {"category_form": category_form, "category": category}
    except Exception as error:
        category_form = CategoryForm(request.POST)
        data = {"category_form": category_form}
        messages.error(request, error)
    return render(request, "vendor/edit_category.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def deltecategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if Category is not None:
        category.delete()
        messages.success(request, "Category deleted successfully")
    else:
        messages.error(request, "category not found")

    return redirect("category")


@login_required(login_url="login")
@user_passes_test(check_vendor)
def addmenu(request):
    if request.method == "POST":
        menu_form = MenuForm(request.POST, request.FILES)
        if menu_form.is_valid():
            vendor = get_vendor(request)
            menu_title = menu_form.cleaned_data["menu_title"]
            menu = menu_form.save(commit=False)
            menu.vendor = vendor
            menu.slug = slugify(menu_title)
            menu.save()
            messages.success(request, "Menu added successfully")
            return redirect("menus_by_category", menu.category.id)
        else:
            print(menu_form.errors)
    else:
        menu_form = MenuForm()
        menu_form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor(request)
        )

    data = {"menu_form": menu_form}
    return render(request, "vendor/add_menu.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def editmenu(request, pk=None):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu_form = MenuForm(request.POST, request.FILES, instance=menu)
        if menu_form.is_valid():
            vendor = get_vendor(request)
            menu_title = menu_form.cleaned_data["menu_title"]
            menu = menu_form.save(commit=False)
            vendor = get_vendor(request)
            menu.vendor = vendor
            menu.slug = slugify(menu_title)
            menu.save()
            messages.success(request, "Menu Updated successfully")
            return redirect("menus_by_category", menu.category.id)
        else:
            print(menu_form.errors)
    else:
        menu_form = MenuForm(instance=menu)
        menu_form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor(request)
        )
    data = {"menu_form": menu_form, "menu": menu}
    return render(request, "vendor/edit_menu.html", data)


@login_required(login_url="login")
@user_passes_test(check_vendor)
def deletemenu(request, pk=None):
    menu = get_object_or_404(Menu, pk=pk)
    if menu is not None:
        menu.delete()
        messages.success(request, "Menu deleted successfully")
    else:
        messages.error(request, "menu not found")

    return redirect("menus_by_category", menu.category.id)
