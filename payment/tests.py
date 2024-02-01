from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Payment, Transaction
from django.contrib.auth import get_user_model
from orders.models import Order
from django.core.exceptions import ValidationError

User = get_user_model()
class PaymentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(id = 1,username='testuser',email = 'test@test.com')
        order = Order.objects.create(id =2 ,customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        Payment.objects.create(id = 1, customer=user, order=order,
                               amount=100.00, status='pending')


    def test_creating_payment(self):
        user = User.objects.create(id = 8,username='testuser_2',email='test_2@test.com')
        order = Order.objects.create(customer=user)
        payment = Payment.objects.create(customer=user, order=order, amount=100.00, status='pending')
        self.assertEqual(payment.customer, user)
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.amount, 100.00)
        self.assertEqual(payment.status, 'pending')

    def test_invalid_amount(self):
        user = User.objects.create(id=9, username='testuser',email='test@test.com')
        order = Order.objects.create(customer=user)
        with self.assertRaises(ValueError):
            Payment.objects.create(customer=user, order=order, amount=-100.00, status='pending')

    def test_invalid_order(self):
        user = User.objects.create(id=1, username='testuser2',email='test2@test.com')
        with self.assertRaises(ValueError):
            Payment.objects.create(customer=user, amount=100.00, status='pending')

    def test_create_payment_with_missing_customer(self):
        order = Order.objects.create(customer=None)
        with self.assertRaises(ValidationError):
            Payment.objects.create(order=order, amount=100.00, status='pending')


class TransactionModelTests(TestCase):

    def test_creating_transaction(self):
        
        payment = Payment.objects.create(id=2, amount=100, status='pending')
        transaction = Transaction.objects.create(id=1,
            payment=payment, name='John Doe', address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')
        self.assertEqual(transaction.payment, payment)
        self.assertEqual(transaction.name, 'John Doe')
        self.assertEqual(transaction.address1, '123 Main Street')
        self.assertEqual(transaction.address2, None)
        self.assertEqual(transaction.city, 'Anytown')
        self.assertEqual(transaction.state, 'CA')
        self.assertEqual(transaction.zip_code, '90210')

    def test_transaction_state_choices(self):
        self.assertEqual(Transaction.STATE_CHOICES, ((
            'pe', 'Pending'),
            ('pr', 'Processing'),
            ('pa', 'Paid'),
            ('fa', 'Failed'),
            ('re', 'Refunded'),
        ))

    def test_invalid_state(self):
        with self.assertRaises(ValidationError):
            Transaction.objects.create(id=3,
            payment=None, name='John Doe', address1='123 Main Street', city='Anytown', state='AA', zip_code='90210'
            )

    def test_transaction_with_missing_payment(self):
       
        with self.assertRaises(ValidationError):
            Transaction.objects.create(id = 4,
                 name='John Doe', address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')

    def test_transaction_with_missing_customer(self):
        payment = Payment.objects.create(id=5, amount=100, status='pending')
        with self.assertRaises(ValidationError):
            Transaction.objects.create(id=1 ,payment=payment, name='John Doe',
                                       address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')
