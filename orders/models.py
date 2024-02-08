from django.db import models
from products.models import Product
from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# Create your models here.


class Order(BaseModel):
    """
    Reprisent orders of customers
    """
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.uuid}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(BaseModel):
    order = models.ForeignKey(Order,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                   related_name='order_items',
                                   on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Payment(BaseModel):
    """
    Payment of orders 
    """
    # Payment use
    order_id = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                 MinValueValidator(0)])

    status = models.CharField(max_length=10, choices=(
        ('pe', 'Pending'),
        ('pr', 'Processing'),
        ('pa', 'Paid'),
        ('fad', 'Failed'),
        ('re', 'Refunded'),
    ))

    def validate_amount(self):
        if self.amount < 0:
            raise ValueError('Amount cannot be negative.')


class Transaction(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
