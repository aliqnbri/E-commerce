from rest_framework import serializers
from product.models import Category , Product , Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='product-detail', lookup_field='slug')
    class Meta:
        model = Product
        fields = ['name' ,'brand','description', 'price', 'review','category', 'get_absolute_url']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        
