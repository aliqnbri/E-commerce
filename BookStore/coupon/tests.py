from django.test import TestCase
from .models import Coupon

from products.models import Product, Author
# Create your tests here.


class CouponTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Harper', last_name='Lee', bio='American novelist, playwright, and activist.')
        self.product = Product.objects.create(
            title="Test Product", price=100.00,author=self.author)
        self.discount_percent = Coupon.objects.create(
            product=self.product, discount_percent=10)
        self.discount_amount = Coupon.objects.create(
            product=self.product, discount_amount=20)

    def test_discounted_price_with_percent(self):
        discounted_price = self.discount_percent.calculate_discounted_price()
        self.assertEqual(discounted_price, 90.00)

    def test_discounted_price_with_amount(self):
        discounted_price = self.discount_amount.calculate_discounted_price()
        self.assertEqual(discounted_price, 80.00)

    def test_no_discount(self):
        no_discount = Coupon.objects.create(product=self.product)
        no_discounted_price = Coupon.calculate_discounted_price()
        self.assertEqual(no_discounted_price, 100.00)


# class CouponTest(TestCase):

#     def test_create_coupon(self):
#         coupon = Coupon.objects.create(
#             code='123456',
#             discount_amount=10.0,
#             expiration_date='2023-10-04',
#             is_active=True
#         )

#         self.assertEqual(coupon.code, '123456')
#         self.assertEqual(coupon.discount_amount, 10.0)
#         self.assertEqual(coupon.expiration_date, '2023-10-04')
#         self.assertEqual(coupon.is_active, True)

#     def test_validate_coupon_code_length(self):
#         with self.assertRaises(ValidationError):
#             Coupon.objects.create(code='123', discount_amount=10.0,
#                                   expiration_date='2023-10-04', is_active=True)

#     def test_validate_discount_value(self):
#         with self.assertRaises(ValidationError):
#             Coupon.objects.create(
#                 code='123456', discount=-10.0, expiration_date='2023-10-04', is_active=True)

#     def test_validate_expiration_date(self):
#         with self.assertRaises(ValidationError):
#             Coupon.objects.create(
#                 code='123456', discount=10.0, expiration_date='2022-10-04', is_active=True)

#     def test_validate_is_active_value(self):
#         with self.assertRaises(ValidationError):
#             Coupon.objects.create(
#                 code='123456', discount=10.0, expiration_date='2023-10-04', is_active=False)
