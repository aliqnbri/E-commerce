from django.db import models
import uuid


# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True




class ShopInfo(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name='Shop Name')
    address = models.CharField(max_length=255, verbose_name='Address')
    phone_number = models.CharField(max_length=12, verbose_name='Phone Number')
    locations = models.TextField(verbose_name='Locations')
    extra = models.TextField(verbose_name='Extra Info')