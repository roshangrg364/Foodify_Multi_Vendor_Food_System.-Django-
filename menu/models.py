from django.db import models
from vendor.models import Vendor

# Create your models here.


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(
        max_length=100, unique=True, blank=False, null=False
    )
    category_slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, unique=True, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name


class Menu(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    menu_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300)
    description = models.TextField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="foodimages")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.menu_title
