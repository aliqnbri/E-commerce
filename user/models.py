from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.db import models

# models.PhoneNumberField(_(""))
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('operator', 'Operator'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email