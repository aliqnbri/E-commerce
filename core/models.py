from django.db import models
import uuid


# Create your models here.

class SoftDeleteManager(models.Manager):
    def delete(self, *args, **kwargs):
        if kwargs.get('force_delete', False):
            super().delete(*args, **kwargs)
        else:
            for obj in self.get_queryset(*args, **kwargs):
                obj.is_deleted = True
                obj.save()


class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    class Meta:
        abstract = True




class ShopInfo(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name='Shop Name')
    address = models.CharField(max_length=255, verbose_name='Address')
    phone_number = models.CharField(max_length=12, verbose_name='Phone Number')
    locations = models.TextField(verbose_name='Locations')
    extra = models.TextField(verbose_name='Extra Info')