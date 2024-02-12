
from .models import Category, Author, Review, Product
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTestCase(TestCase):
    def setUp(self):
        # Create test data for models
        self.category = Category.objects.create(
            name='Test Category', slug='test-category', description='products of fantasy genre' ,parent=None, image= 'media/catgories/test.jpg')
        self.author = Author.objects.create(
            first_name='John', last_name='Doe', slug='john-doe', bio='lives in Tehran')

        self.product = Product.objects.create(title='Test Product', slug='test-product', author=self.author,
                                              isbn='123456789', price=10.00, available=True, description='some description')
        self.product.categories.add(self.category)
        
        
        self.user = User.objects.create(
            username='testuser', email='test@example.com')
        self.review = Review.objects.create(
            user=self.user, product=self.product, rating=5, comment='Great product!')

    def test_product_model(self):
        """
        Test product 
        """
        
        product = Product.objects.get(slug='test-product')
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.author, self.author)
        self.assertEqual(self.product.author.first_name, 'John')
        self.assertEqual(self.product.author.last_name, 'Doe')
        self.assertEqual(product.isbn, '123456789')
        self.assertEqual(self.product.price, 10.00)
        self.assertTrue(self.product.available)
        self.assertEqual(self.product.description, 'some description')
        self.assertEqual(self.product.categories.first().name, 'Test Category')
        self.assertEqual(str(self.product), 'Test Product')

    def test_category_products(self):
        category = Category.objects.get(name='Test Category')
        products = category.product_set.all()
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().title, 'Test Product')


    def test_category_model(self):
        """
        Geting a category object for testing purposes.
        """
        category = Category.objects.get(slug='test-category')
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.image, 'media/catgories/test.jpg')
        self.assertEqual(self.category.description,'products of fantasy genre')
        self.assertTrue(self.category.slug == 'test-category')
        self.assertIsNone(self.category.parent)
        self.assertEqual(self.category._meta.verbose_name, 'category')
        self.assertEqual(self.category._meta.verbose_name_plural, 'categories')

    def test_category_save(self):
        """
        Checks if saving a category updates the slug.
        """
        self.category.name = 'Science Fiction'
        self.category.save()
        self.assertTrue(self.category.slug == 'science-fiction')

    def test_review_model(self):
        """ Test Review Model """
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great product!')

    def test_author_model(self):
        """
        Test Author Model 
        """
        self.assertEqual(self.author.first_name, 'John')
        self.assertEqual(self.author.last_name, 'Doe')
        self.assertEqual(self.author.slug, 'john-doe')
        self.assertEqual(self.author.bio, 'lives in Tehran')

   