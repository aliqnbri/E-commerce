from django.test import TestCase
from .models import Coupon

# Create your tests here.



class CouponTest(TestCase):

    def test_create_coupon(self):
        coupon = Coupon.objects.create(
            code='123456',
            discount=10.0,
            expiration_date='2023-10-04',
            is_active=True
        )

        self.assertEqual(coupon.code, '123456')
        self.assertEqual(coupon.discount, 10.0)
        self.assertEqual(coupon.expiration_date, '2023-10-04')
        self.assertEqual(coupon.is_active, True)

    def test_validate_coupon_code_length(self):
        with self.assertRaises(ValidationError):
            Coupon.objects.create(code='123', discount=10.0,
                                  expiration_date='2023-10-04', is_active=True)

    def test_validate_discount_value(self):
        with self.assertRaises(ValidationError):
            Coupon.objects.create(
                code='123456', discount=-10.0, expiration_date='2023-10-04', is_active=True)

    def test_validate_expiration_date(self):
        with self.assertRaises(ValidationError):
            Coupon.objects.create(
                code='123456', discount=10.0, expiration_date='2022-10-04', is_active=True)

    def test_validate_is_active_value(self):
        with self.assertRaises(ValidationError):
            Coupon.objects.create(
                code='123456', discount=10.0, expiration_date='2023-10-04', is_active=False)
