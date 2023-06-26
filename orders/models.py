from django.db import models
from accounts.models import User
from menu.models import Menu
from vendor.models import Vendor
import json

request_object = ""


class Payment(models.Model):
    Status_Pending = "Pending"
    Status_Completed = "Completed"

    PaymentMethod_Paypal = "PayPal"
    PaymentMethod_CashOnDelivery = "CashOnDelivery"

    PAYMENT_METHOD = (
        (PaymentMethod_Paypal, PaymentMethod_Paypal),
        (PaymentMethod_CashOnDelivery, PaymentMethod_CashOnDelivery),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    Status_New = "New"
    Status_Received = "Received"
    Status_Completed = "Completed"
    Status_Cancelled = "Cancelled"

    STATUS = (
        (Status_New, Status_New),
        (Status_Received, Status_Received),
        (Status_Completed, Status_Completed),
        (Status_Cancelled, Status_Cancelled),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(
        blank=True,
        help_text="Data format: ['tax_type','tax_percentage','tax_amount']",
    )
    total_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Data format: {'vendor_id':{'subtotal':'tax_data'}}]",
    )
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default="New")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def vendors_list(self):
        return ",".join(str(i) for i in self.vendors.all())

    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        total_data = json.loads(
            self.total_data
        )  # json format {"vendor_id":{subtotal:[{"tax_type":"GST","tax_percentage":13,"tax_amount":300]}
        data = total_data.get(str(vendor.id))
        sub_total = 0
        tax = 0
        tax_data = []
        for key, val in data.items():
            sub_total += float(key)
            tax_data = val
        for tax_value in tax_data:
            tax += float(tax_value["tax_amount"])

        grand_total = sub_total + tax

        data = {
            "tax_data": tax_data,
            "sub_total": sub_total,
            "total_tax": tax,
            "grand_total": grand_total,
        }
        return data

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu.menu_title
