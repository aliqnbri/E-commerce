from django.test import TestCase
from coupon.models import Coupon
from product.models import Product, Author

from datetime import date
# Create your tests here.


class CouponModelTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name='John', last_name='Doe', slug='john-doe', bio='lives in Tehran')
        self.product = Product.objects.create(title='Test Product', slug='test-product', author=self.author,
                                              isbn='123456789', price=100.00, available=True, description='some description')
        self.coupon_percent = Coupon.objects.create(
            product=self.product, code='TEST1', discount_percent=10, expiration_date=date.today())
        self.coupon_amount = Coupon.objects.create(
            product=self.product, code='TEST2', discount_amount=20, expiration_date=date.today())

    def test_calculate_discounted_price_percent(self):
        discounted_price = self.coupon_percent.calculate_discounted_price()
        expected_price = 100.00 * (1 - (10/100))  # 10% discount
        self.assertEqual(discounted_price, expected_price)

    def test_calculate_discounted_price_amount(self):
        discounted_price = self.coupon_amount.calculate_discounted_price()
        expected_price = 100.00 - 20.00  # $20 discount
        self.assertEqual(discounted_price, expected_price)

    def test_calculate_discounted_price_no_discount(self):
        no_discount_coupon = Coupon.objects.create(
            product=self.product, code='TEST3', expiration_date=date.today())
        discounted_price = no_discount_coupon.calculate_discounted_price()
        self.assertEqual(discounted_price, 100.00)  # No discount applied

    def test_coupon_is_active(self):
        active_coupon = Coupon.objects.create(
            product=self.product, code='TEST4', is_active=True, expiration_date=date.today())
        self.assertTrue(active_coupon.is_active)

    def test_coupon_is_not_active(self):
        inactive_coupon = Coupon.objects.create(
            product=self.product, code='TEST5', is_active=False, expiration_date=date.today())
        self.assertFalse(inactive_coupon.is_active)
