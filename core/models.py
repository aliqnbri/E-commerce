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

import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    class Meta:
        abstract = True
    STATUS_CHOICES = (
        ('dr', 'Draft'),
        ('pu', 'Published'),
        ('ar', 'Archived'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='dr')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Set the abstract attribute to True to indicate that this model is intended to be used as a base class and not as a concrete model

    # def save(self, *args, **kwargs):
    #     # Add custom logic before saving the model
    #     super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"{self.__class__.__name__} - {self.uuid}"


