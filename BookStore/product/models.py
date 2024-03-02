from django.db import models
from core.models import BaseModel
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.urls import reverse

# <p class="tags">Tags: {{ catgory.tags.all|join:", " }}</p>
# Create your models here.

User = get_user_model()

class Category(BaseModel):
    """
    A Django model representing a book category in an online bookstore.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='media/catgories/',
                              height_field=None, width_field=None, max_length=None)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')
    class Meta:

        """
        Meta class for the Category model.
        """
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('product:product_list_by_category',
                       args=[self.slug])
    def __str__(self):
        return self.name

    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)


class Author(BaseModel):
    """
    A Django model representing a book author in an online bookstore.
    """
    first_name = models.CharField(
        max_length=255, verbose_name="Author's First Name")
    last_name = models.CharField(
        max_length=255, verbose_name="Author's Last Name")
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name="Author Slug")
    bio = models.TextField(blank=True, verbose_name="Author's Bio")

    def __str__(self):
        """
        Returns the string representation of the Author object.
        """
        return f"{self.first_name} {self.last_name}"


class Product(BaseModel):

    """
    A Django model representing a specific product in an online bookstore.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    image = models.ImageField(upload_to='media/products/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        Category)  # Added ForeignKey to Category
    tags = TaggableManager()
    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id,self.slug])

    def __str__(self):
        return self.title


class Review(BaseModel):
    """
    A Django model representing a review for a specific book.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username}"
