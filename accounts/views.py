from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.


def registeruser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.role = User.CUSTOMER
            messages.success(request, "User Registered Successfully")
            user.save()
       
        redirect("accounts/RegisterUser.html")
    else:
        form = UserForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/RegisterUser.html", context)
