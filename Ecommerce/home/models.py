from django.db import models

# Create your models here.


class ShopInfo(models.Model):
    
    name = models.CharField(max_length=255, verbose_name='Shop Name')
    address = models.TextField()
    phone_number = models.CharField(max_length=12, verbose_name='Phone Number')
    locations = models.TextField(verbose_name='Locations')
    extra = models.TextField(verbose_name='Extra Info')
    logo = models.ImageField(upload_to='media/logos/', null=True, blank=True)