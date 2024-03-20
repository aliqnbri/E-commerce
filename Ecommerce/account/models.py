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
    username = None
    phone_number = models.CharField(max_length=11, unique=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True,editable=True,)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='cu')

    USERNAME_FIELD = "email"

    # email and passwrod required by default
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"


class Address(BaseModel):
    """
    Address Model for user's address 
    """
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country} - {self.postal_code}"





class CustomerProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
    user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE)
    username = models.CharField(max_length=16, unique=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    




