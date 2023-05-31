from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def vendorprofile(request):
    return render(request, "vendor/vendorprofile.html")
