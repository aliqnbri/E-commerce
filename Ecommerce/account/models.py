from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from account.utils.managers import CustomUserManager
from core.models import BaseModel
from django.db import models


class CustomUser( AbstractBaseUser, PermissionsMixin,BaseModel):
    ROLE_CHOICES = (
        ('ad', 'Admin'),
        ('op', 'Operator'),
        ('cu', 'Customer'),
    )    
    username = models.CharField(max_length=16, unique=True, null=True,)
    phone_number = models.CharField(max_length=11, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='cu')

    USERNAME_FIELD = "email"

    # email and passwrod required by default
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


    def tokens(self):
        pass    


class Address(BaseModel):
    """
    Address Model for user's address 
    """
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def get_address(self):
        return f"Address : {self.city} ,{self.street}, {self.postal_code}"





class CustomerProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
    user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30,verbose_name='Last Name')
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE )



    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_username(self):
        return f'{self.username}'
    

    



