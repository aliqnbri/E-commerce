from django.db import models
from core.models import BaseModel
from django.core.validators import MinValueValidator, MinValueValidator
from decimal import Decimal
# Create your models here.
class Payment(BaseModel):
    """
    Payment of orders 
    """
    # Payment use
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))])

    status = models.CharField(max_length=10, choices=(
        ('pe', 'Pending'),
        ('pr', 'Processing'),
        ('pa', 'Paid'),
        ('fad', 'Failed'),
        ('re', 'Refunded'),
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
    zip_code = models.CharField(max_length=10)
