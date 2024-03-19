from rest_framework import serializers
from order.models import Order, OrderItem

from django.contrib.auth import get_user_model
User = get_user_model()


class CustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)









class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cost'] = instance.get_cost()
        return representation
    

class CreateOrderItemSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer =  CustomerSerializer(source='User.email',read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'is_completed', 'coupon', 'discount', 'items']

    def get_customer(self,obj):
        return obj.user.username

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
