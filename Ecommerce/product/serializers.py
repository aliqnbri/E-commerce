from rest_framework import serializers
from product.models import Category , Product , Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='slug')
    class Meta:
        model = Product
        fields = ['id','name','brand','available','price','url' ,'category']        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        
