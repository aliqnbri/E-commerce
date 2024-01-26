from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    """
    A Django model representing a book category in an online bookstore.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:

        """
        Meta class for the Category model.
        """
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


class Author(models.Model):
    """
    A Django model representing a book author in an online bookstore.
    """
    first_name = models.CharField(max_length=255, verbose_name="Author's First Name")
    last_name = models.CharField(max_length=255, verbose_name="Author's Last Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Author Slug")
    bio = models.TextField(blank=True, verbose_name="Author's Bio")

    def __str__(self):
        """
        Returns the string representation of the Author object.
        """
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):

    """
    A Django model representing a specific book in an online bookstore.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=13, unique=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='books')  # Added ForeignKey to Category

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


