from django.db import models

# Create your models here.


class ShopInfo(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name='Shop Name')
    address = models.CharField(max_length=255, verbose_name='Address')
    phone_number = models.CharField(max_length=12, verbose_name='Phone Number')
    locations = models.TextField(verbose_name='Locations')
    extra = models.TextField(verbose_name='Extra Info')