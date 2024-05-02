from rest_framework import serializers
from order.models import Order, OrderItem ,Cart
from product.models import Product
from rest_framework import serializers
from decimal import Decimal
from core.models import BaseModel
from coupon.models import Coupon
from account.models import CustomerProfile








class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ('id', 'product_name', 'product_price', 'quantity', 'created')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cost'] = instance.get_cost()
        return representation


class OrderSerializer(serializers.ModelSerializer):
    customer_username = serializers.ReadOnlyField(source='customer.username')
    total_cost = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    coupon_code = serializers.ReadOnlyField(source='coupon.code')
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer_username', 'total_amount', 'total_cost', 'discount_amount', 'coupon_code', 'is_completed', 'discount', 'items', 'created')

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    def get_discount_amount(self, obj):
        return obj.get_discount()

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order



class CartSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total_price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'price',
                  'total_price', 'discount', 'total_price_after_discount']

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_discount(self, obj):
        return obj.get_discount()

    def get_total_price_after_discount(self, obj):
        return obj.get_total_price_after_discount()
