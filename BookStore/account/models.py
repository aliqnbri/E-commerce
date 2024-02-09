from django.db import models
from django.contrib.auth.models import AbstractUser
import re
# Create your models here.

class BaseUser(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ad" , 'Admin'
        OPERATOR = "op" , 'Operator'
        CUSTOMER = "cu" , 'Customer'
    phone_number = models.CharField(max_length=13, unique=True)
    base_role = Role.ADMIN


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def clean(self):
        if not re.match(r'^\+98\d{10}$', self.phone_number):
            raise ValidationError(
                "Invalid phone number format for Iran. It should start with '+98' followed by 10 digits.")

    def __str__(self):
        return self.uuid



class Customer(BaseUser):
    base_role = BaseUser.Role.CUSTOMER 


    class Meta:
        proxy = True











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

