from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from account.utils.managers import CustomUserManager
from core.models import BaseModel
from django.db import models


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ad', 'Admin'),
        ('op', 'Operator'),
        ('cu', 'Customer'),
    )    
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, unique=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True,editable=True,)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='cu')

    USERNAME_FIELD = "email"

    # email and passwrod required by default
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"


class CustomerProfile(BaseModel):
    user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE)
    #todo -> first_name last_name 
    



class Address(BaseModel):
    """
    Address Model for user's address 
    """
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country} - {self.postal_code}"
