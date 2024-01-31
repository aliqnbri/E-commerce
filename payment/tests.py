from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Payment, Transaction
from django.contrib.auth import get_user_model
from orders.models import Order
from django.core.exceptions import ValidationError


class PaymentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = get_user_model().objects.create(id = 1,username='testuser')
        order = Order.objects.create(id =1 ,customer=user, first_name='John', last_name='Doe',
                                     address='123 Main Street', postal_code='12345', city='Anytown')
        Payment.objects.create(id = 1, customer=user, order=order,
                               amount=100.00, status='pending')

    def test_customer_label(self):
        payment = Payment.objects.get(id=1)
        field_label = payment._meta.get_field('customer').verbose_name
        self.assertEquals(field_label, 'customer')

    def test_order_label(self):
        payment = Payment.objects.get(id=1)
        field_label = payment._meta.get_field('order').verbose_name
        self.assertEquals(field_label, 'order')

    def test_amount_label(self):
        payment = Payment.objects.get(id=1)
        field_label = payment._meta.get_field('amount').verbose_name
        self.assertEquals(field_label, 'amount')

    def test_status_label(self):
        payment = Payment.objects.get(id=1)
        field_label = payment._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')


class TransactionModelTests(TestCase):

    def test_creating_transaction(self):
        user = get_user_model().objects.create(id=1, username='testuser')
        payment = Payment.objects.create(id=1, amount=100, status='pending')
        transaction = Transaction.objects.create(id=1,
            customer=user, payment=payment, name='John Doe', address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')
        self.assertEqual(transaction.customer, user)
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
            Transaction.objects.create(id=1,
                customer=None, payment=None, name='John Doe', address1='123 Main Street', city='Anytown', state='AA', zip_code='90210'
            )

    def test_transaction_with_missing_payment(self):
        user = get_user_model().objects.create(id=1,username='testuser')
        with self.assertRaises(ValidationError):
            Transaction.objects.create(id = 1,
                customer=user, name='John Doe', address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')

    def test_transaction_with_missing_customer(self):
        payment = Payment.objects.create(id=1, amount=100, status='pending')
        with self.assertRaises(ValidationError):
            Transaction.objects.create(id=1 ,payment=payment, name='John Doe',
                                       address1='123 Main Street', city='Anytown', state='CA', zip_code='90210')
