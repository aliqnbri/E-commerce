# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.password_validation import validate_password
# from account.models import CustomUser, CustomerProfile
# from rest_framework.validators import UniqueValidator
# from rest_framework import serializers
# from product.models import Category , Product , Review
# from coupon.models import Coupon


# class CouponSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Coupon
#         fields = ['id', 'product', 'code', 'discount', 'discount_amount', 'expiration_date', 'valid_from', 'is_active']

#     def calculate_discounted_price(self, obj):
#         if obj.discount_percent is not None:
#             return obj.product.price * (1 - (obj.discount_percent / 100))
#         elif obj.discount_amount is not None:
#             return obj.product.price - obj.discount_amount
#         else:
#             return obj.product.price        