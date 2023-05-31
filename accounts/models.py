from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Email is required")

        if not username:
            raise ValueError("username is required")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            last_name=last_name,
            first_name=first_name,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True

        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = ((VENDOR, "Vendor"), (CUSTOMER, "Customer"))

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=50, blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = "Vendor"
        elif self.role == 2:
            user_role = "Customer"
        return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photos", blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=100, null=True, blank=True)
    Longitude = models.CharField(max_length=100, null=True, blank=True)
    Latitude = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def full_address(self):
        return f"{self.address_line_1},{self.address_line_2}"
