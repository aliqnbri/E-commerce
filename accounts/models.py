from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
from core.models import BaseModel
from django.db import models
import re


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # can login
    ROLE_CHOICES = (
        ('ad', 'Admin'),
        ('op', 'Operator'),
        ('cu', 'Customer'),
    )

    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='cu')
    USERNAME_FIELD = "email"

    # email and passwrod required by default
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # def clean(self):
    #     if not re.match(r'^[\w.@+-]+$', self.username):
    #             raise ValidationError(
    #                 "Invalid characters in the username. Use only letters, numbers, and @/./+/-/_ characters.")

    def __str__(self):
        if self.username:
            return self.username
        return self.USERNAME_FIELD


class Address(BaseModel):
    """
    Address Model for user's address 
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country} - {self.postal_code}"
