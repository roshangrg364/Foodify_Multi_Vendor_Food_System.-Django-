from django import forms
from .models import vendor


class VendorForm(forms.ModelForm):
    password: forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = vendor
        fields = ["vendor_name", "vendor_license"]
