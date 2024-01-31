from django.db import models

from core.models import BaseModel
# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Payment(BaseModel):
    # Payment user
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Payment order
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=10, choices=(
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ))
    

class Transaction(BaseModel):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=(
        ('pe', 'Pending'),
        ('pr', 'Processing'),
        ('pa', 'Paid'),
        ('fa', 'Failed'),
        ('re', 'Refunded'),
    ))
    zip_code = models.CharField(max_length=10)
    
