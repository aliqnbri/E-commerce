from decimal import Decimal
from django.core.validators import MinValueValidator, \
    MaxValueValidator
from django.db import models
from product.models import Product
from core.models import BaseModel
from coupon.models import Coupon
from account.models import CustomerProfile
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from rest_framework import serializers


class Order(BaseModel):
    """
    Reprisent orders of customers
    """
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='order_set',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_username(self):
        if self.customer.username:
            return self.customer.username
        return self.user.email


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
        return f"Order Item #{self.id} - Product: {self.product}, Quantity: {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity


class Cart(BaseModel):
    user = models.ForeignKey(CustomerProfile,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cart {self.id}'

    def get_total_price(self):
        return self.quantity * self.price

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
