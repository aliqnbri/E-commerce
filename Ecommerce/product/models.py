from django.db import models
from core.models import BaseModel
from django.utils.text import slugify
from mptt.models import TreeForeignKey, MPTTModel
from account.models import CustomerProfile


class Category(MPTTModel,BaseModel):
    """
    A Django model representing a book category in an online bookstore.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')
    class MPTTMeta:

        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)

class Brand(BaseModel):
    name = models.CharField(max_length=200)



class Review(BaseModel):
    """
    A Django model representing a review for a specific book.
    """
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.CustomerProfile.username} commets:{self.comment}"


class Product(MPTTModel,BaseModel):

    """
    A Django model representing a specific product in an online bookstore.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE )
    image = models.ImageField(upload_to='media/products/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviews')
    # category = TreeForeignKey('Category',null=True,blank=True,on_delete=models.SET_NULL)  # Added ForeignKey to Category
    class Meta:
        ordering = ('name',)


    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)


    def __str__(self):
        return self.title


class WishList(models.Model):
    user = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)