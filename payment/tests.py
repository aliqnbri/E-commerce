from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Payment, Transaction
from django.contrib.auth import get_user_model
from . import models


class PaymentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = get_user_model().objects.create(username='testuser')
        order = models.Order.objects.create(
            order_number='12345', total_amount=100.00)
        Payment.objects.create(customer=user, order=order,
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


class TransactionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username='testuser')
        order = models.Order.objects.create(
            order_number='12345', total_amount=100.00)
        payment = Payment.objects.create(
            customer=user, order=order, amount=100.00, status='pending')
        Transaction.objects.create(customer=user, payment=payment, name='Test Name',
                                   address1='Address 1', address2='Address 2', city='City', state='pe', zip_code='12345')

    def test_customer_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('customer').verbose_name
        self.assertEquals(field_label, 'customer')

    def test_payment_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('payment').verbose_name
        self.assertEquals(field_label, 'payment')

    def test_name_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_state_label(self):
        transaction = Transaction.objects.get(id=1)
        field_label = transaction._meta.get_field('state').verbose_name
        self.assertEquals(field_label, 'state')
