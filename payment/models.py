from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel
from decimal import Decimal

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Payment(BaseModel):
    # Payment user
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Payment order
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
    
    status = models.CharField(max_length=10, choices=(
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ))
    def validate_amount(self):
        if self.amount < Decimal('0.00'):
            raise ValueError('Amount cannot be negative.')

class Transaction(BaseModel):
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
    
