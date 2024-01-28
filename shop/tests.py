from .models import Book
from .models import Category, Author, Review, Book
from django.test import TestCase

# Create your tests here.


class CategoryTest(TestCase):

    def setUp(self):
        """
        Creates a category object for testing purposes.
        """
        self.category = Category.objects.create(
            name='Fantasy', description='Books of fantasy genre')

    def test_category_creation(self):
        """
        Checks if the category was created successfully.
        """
        self.assertEqual(self.category.name, 'Fantasy')
        self.assertEqual(self.category.description, 'Books of fantasy genre')
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
            first_name='J.K.', last_name='Rowling', bio='Famous author of the Harry Potter series.')

    def test_author_creation(self):
        """
        Checks if the author was created successfully.
        """
        self.assertEqual(self.author.first_name, 'J.K.')
        self.assertEqual(self.author.last_name, 'Rowling')
        self.assertTrue(self.author.slug == 'j-k-rowling')

    def test_author_unique_name(self):
        """
        Checks if an author name is unique.
        """
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                first_name='J.K.', last_name='Rowling', bio='Another bio')
