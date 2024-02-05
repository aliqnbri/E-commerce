from django.test import TestCase
from core.models import BaseModel
from products.models import Category, Author, Review, Product
from .models import Order, Order, OrderItem
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist ,ValidationError



# Create your tests here.

User = get_user_model()

class OrderModelTests(TestCase):

    def test_creating_order(self):
        user = User.objects.create(username='testuser',)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        self.assertEqual(order.customer, user)
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.address, '123 Main Street')
        self.assertEqual(order.postal_code, '12345')
        self.assertEqual(order.city, 'Anytown')
        self.assertFalse(order.paid)

    def test_getting_total_cost(self):
        user = User.objects.create(username='testuser')
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)
        order_item1 = OrderItem.objects.create(
            order=order, quantity=2, product=product, price=10.00)
        product_2 = Product.objects.create(
            title='Product 2', price=20.00, author=author)
        order_item2 = OrderItem.objects.create(
            order=order, quantity=1, product=product_2, price=20.00)

        self.assertEqual(get_total_cost(), 40.00)

    def test_order_item_quantity_must_be_positive(self):
        user = User.objects.create(username='testuser',)
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')

        # Try creating order item with negative quantity
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(
                order=order, product=product, quantity=-1, price=20.00)

        # Try creating order item with 0 quantity
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(
                order=order, product=product, quantity=0, price=20.00)

    def test_order_item_cannot_be_created_for_non_existing_order(self):
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)

        with self.assertRaises(ObjectDoesNotExist):
            OrderItem.objects.create(
                order=None, product=product, quantity=1, price=20.00)

    def test_order_item_cannot_be_created_for_non_existing_product(self):
        user = User.objects.create(username='testuser',)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')

        with self.assertRaises(ObjectDoesNotExist):
            OrderItem.objects.create(
                order=order, product=None, quantity=1, price=20.00)










class OrderModelTests(TestCase):

    def test_creating_order(self):
        user = User.objects.create(username='testuser',)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        self.assertEqual(order.customer, user)
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.address, '123 Main Street')
        self.assertEqual(order.postal_code, '12345')
        self.assertEqual(order.city, 'Anytown')
        self.assertFalse(order.paid)

    def test_getting_total_cost(self):
        user = User.objects.create(username='testuser')
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)
        order_item1 = OrderItem.objects.create(
            order=order, quantity=2, product=product, price=10.00)
        product_2 = Product.objects.create(
            title='Product 2', price=20.00, author=author)
        order_item2 = OrderItem.objects.create(
            order=order, quantity=1, product=product_2, price=20.00)

        self.assertEqual(get_total_cost(), 40.00)

    def test_order_item_quantity_must_be_positive(self):
        user = User.objects.create(username='testuser',)
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')

        # Try creating order item with negative quantity
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(
                order=order, product=product, quantity=-1, price=20.00)

        # Try creating order item with 0 quantity
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(
                order=order, product=product, quantity=0, price=20.00)

    def test_order_item_cannot_be_created_for_non_existing_order(self):
        author = Author.objects.create(
            first_name='J.K', last_name='Rowling', bio='Famous author of the Harry Potter series.')
        product = Product.objects.create(
            title='Product 1', price=10.00, author=author)

        with self.assertRaises(ObjectDoesNotExist):
            OrderItem.objects.create(
                order=None, product=product, quantity=1, price=20.00)

    def test_order_item_cannot_be_created_for_non_existing_product(self):
        user = User.objects.create(username='testuser',)
        order = Order.objects.create(customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')

        with self.assertRaises(ObjectDoesNotExist):
            OrderItem.objects.create(
                order=order, product=None, quantity=1, price=20.00)
