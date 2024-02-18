from django.db import models
from core.managers import SoftDeleteManager


class BaseModel(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'on' , 'Active'
        DEACTIVE = 'off', 'Deactive'


    created = models.DateTimeField(auto_now_add=True ,editable=False)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=8,  choices=Status.choices, default=Status.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()


    def delete(self):
        self.is_deleted = True
        self.save()

    def resore(self):
        self.is_deleted = False
        self.save()    

    
    class Meta:
        abstract = True  

    

