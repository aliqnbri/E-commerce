from django.test import TestCase
from decimal import Decimal

# Create your tests here.
from payment.models import Payment, Transaction
from order.models import Order, OrderItem
from django.contrib.auth import get_user_model
from product.models import Author , Product
User = get_user_model()



class PaymentTransactionModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@user.com", password="foo" ,username='testuser')
        self.author = Author.objects.create(
            first_name='John', last_name='Doe', slug='john-doe', bio='lives in Tehran')    
        self.product = Product.objects.create(title='Test Product', slug='test-product', author= self.author,
                                              isbn='123456789', price=10.00, available=True, description='some description')    
        self.order = Order.objects.create(customer=self.user, total_amount=100.00, is_completed=False)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, price=50.00, quantity=2)    
        self.payment = Payment.objects.create(user=self.user, order=self.order, amount=50.00, status='pe')
        self.transaction = Transaction.objects.create(order=self.order, payment=self.payment, zip_code='12345', description='Test transaction')

    def test_payment_model(self):
        self.assertEqual(self.payment.user.email,'customer@user.com')
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.amount, Decimal('50.00'))
        self.assertEqual(self.payment.status, 'pe')
        self.assertEqual(str(self.payment), f'Transaction #{self.payment.id} - User: {self.user.username}, Amount: {self.payment.amount}, Status: {self.payment.status}')

    def test_transaction_model(self):
        self.assertEqual(self.transaction.order, self.order)
        self.assertEqual(self.transaction.payment, self.payment)
        self.assertEqual(self.transaction.zip_code, '12345')
        self.assertEqual(self.transaction.description, 'Test transaction')