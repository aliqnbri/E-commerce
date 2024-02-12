from django.test import TestCase
from core.models import BaseModel
from product.models import Category, Author, Review, Product
from order.models import Order, OrderItem
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist ,ValidationError

from decimal import Decimal
       

# Create your tests here.

User = get_user_model()



class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@admin.com", password="foo" ,username='testuser')

        self.category = Category.objects.create(
            name='Test Category', slug='test-category', description='products of fantasy genre' ,parent=None, image= 'media/catgories/test.jpg')
        self.author = Author.objects.create(
            first_name='John', last_name='Doe', slug='john-doe', bio='lives in Tehran')    
        self.product = Product.objects.create(title='Test Product', slug='test-product', author=self.author,
                                              isbn='123456789', price=10.00, available=True, description='some description')    
        self.order = Order.objects.create(customer=self.user, total_amount=100.00, is_completed=False)
    
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, price=50.00, quantity=2)
    
    def test_order_total_cost(self):
        order = Order.objects.get(customer__username='testuser')
        self.assertEqual(order.get_total_cost(), 100.00)  # Add appropriate calculations based on OrderItem
        self.assertEqual(order.is_completed, False)  # Add appropriate calculations based on OrderItem


    def test_order_item_cost(self):
        order_item = OrderItem.objects.get(product__title='Test Product')
        self.assertEqual(order_item.get_cost(), 100.00)  # Price * Quantity calculation

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(product__title='Test Product')
        self.assertEqual(str(order_item), "Order Item #1 - Product: Test Product, Quantity: 2")

