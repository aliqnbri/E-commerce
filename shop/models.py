from django.db import models

# Create your models here.
class Category(models.Model):
    """
    A Django model representing a category in a content management system.
    """
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 200, unique = True)

    class Meta:

        """
        Meta class for the Category model.
        """
        ordering = ['name']
        indexes = [models.Index(fields = ['name'])]
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
    



from django.utils.text import slugify

class Product(models.Model):
    """
    A Django model representing a product in an e-commerce application.
    """

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Product Category"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Product Name"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Product Slug"
    )

    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name="Product Image"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Product Description"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Product Price"
    )

    available = models.BooleanField(
        default=True,
        verbose_name="Product Availability"
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Product Creation Date"
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Product Updated Date"
    )

    class Meta:
        """
        Meta class for the Product model.
        """
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """
        Returns the string representation of the Product object.
        """
        return self.name

    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)

