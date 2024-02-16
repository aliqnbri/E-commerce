
from django.db import models
from product.models import Product
from core.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()



class Order(BaseModel):
    """
    Reprisent orders of customers
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.uuid}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


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


