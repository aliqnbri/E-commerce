from rest_framework import serializers
from coupon.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'product', 'code', 'discount', 'discount_amount', 'expiration_date', 'valid_from', 'is_active']



class CartAddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    override = serializers.BooleanField(required=False)
