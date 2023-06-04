from django import forms
from .models import Category, Menu
from accounts.validations import validate_images


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class MenuForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info w-100"}),
        validators=[validate_images],
    )

    class Meta:
        model = Menu
        fields = [
            "category",
            "menu_title",
            "description",
            "price",
            "image",
            "is_available",
        ]
