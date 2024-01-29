from django.db import models

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)