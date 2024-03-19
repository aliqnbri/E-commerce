from django.db import models
from core.models import BaseModel
from django.core.validators import MinValueValidator, MinValueValidator
from decimal import Decimal
from django.contrib.auth import get_user_model
from order.models import Order

User = get_user_model()


class Payment(BaseModel):
    """
    Payment of orders 
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
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

    def __str__(self):
        return f'Transaction #{self.id} - User: {self.user.username}, Amount: {self.amount}, Status: {self.status}'


class Transaction(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    description = models.TextField()
