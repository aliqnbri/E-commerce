
from .models import Category, Author, Review, Product
from django.test import TestCase
from django.db import IntegrityError

# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

class CategoryTest(TestCase):

    def setUp(self):
        """
        Creates a category object for testing purposes.
        """
        self.category = Category.objects.create(
            name='Fantasy', description='products of fantasy genre')

    def test_category_creation(self):
        """
        Checks if the category was created successfully.
        """
        self.assertEqual(self.category.name, 'Fantasy')
        self.assertEqual(self.category.description, 'products of fantasy genre')
        self.assertTrue(self.category.slug == 'fantasy')

    def test_category_unique_name(self):
        """
        Checks if a category name is unique.
        """
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='Fantasy', description='Another description')

    def test_category_save(self):
        """
        Checks if saving a category updates the slug.
        """
        self.category.name = 'Science Fiction'
        self.category.save()
        self.assertTrue(self.category.slug == 'science-fiction')


class AuthorTest(TestCase):

    def setUp(self):
        """
        Creates an author object for testing purposes.
        """
        self.author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')

    def test_author_creation(self):
        """
        Checks if the author was created successfully.
        """
        self.assertEqual(self.author.first_name, 'J.K')
        self.assertEqual(self.author.last_name, 'Rowling')
        self.assertFalse(self.author.slug =='jk-rowling')

    def test_author_unique_name(self):
        """
        Checks if an author name is unique.
        """
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                first_name='J.K', last_name='Rowling', bio='Another bio')


class ProductTest(TestCase):

    def setUp(self):
        """
        Creates a product object for testing purposes.
        """
        self.author = Author.objects.create(
            first_name='Harper', last_name='Lee', bio='American novelist, playwright, and activist.')
        category = Category.objects.create(
            name='Classics', description='Classic Literature')
        # self.categoty = Product.categories(category) 

        self.product = Product.objects.create(title='To Kill a Mockingbird', author=self.author, isbn='978-0-449-50420-7', image='covers/products/cover.jpg',
                                           description='A coming-of-age story about a young girl growing up in the American South during the 1930s.', price=17.99, available=True)

    def test_product_creation(self):
        """
        Checks if the product was created successfully.
        """
        self.assertEqual(self.product.title, 'To Kill a Mockingbird')
        self.assertEqual(self.product.author.first_name, 'Harper')
        self.assertEqual(self.product.author.last_name, 'Lee')
        self.assertTrue(self.product.isbn == '978-0-449-50420-7')
        self.assertTrue(self.product.image == 'covers/products/cover.jpg')
        self.assertEqual(self.product.description,
                         'A coming-of-age story about a young girl growing up in the American South during the 1930s.')
        self.assertEqual(self.product.price, 17.99)
        self.assertTrue(self.product.available)


class ReviewTest(TestCase):

    def setUp(self):
        """
        Creates a product object for testing purposes.
        """
        self.product = Product.objects.create(title='To Kill a Mockingbird', author=Author.objects.create(first_name='Harper', last_name='Lee', bio='American novelist, playwright, and activist.'),
                                        isbn='978-0-449-50420-7', image='covers/products/cover.jpg', description='A coming-of-age story about a young girl growing up in the American South during the 1930s.', price=17.99, available=True)

    def test_review_creation(self):
        """
        Checks if a review can be created successfully for a specific product.
        """
        rating = 5
        comment = 'An excellent product!'

        review = Review.objects.create(product=self.product, user=User.objects.create(
            username='user1'), rating=rating, comment=comment)

        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, User.objects.get(username='user1'))
        self.assertEqual(review.rating, rating)
        self.assertEqual(review.comment, comment)
