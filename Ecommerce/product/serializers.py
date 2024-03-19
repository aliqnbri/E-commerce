from rest_framework import serializers
from product.models import Category , Product , Review
from rest_framework.reverse import reverse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='slug')
    class Meta:
        model = Product
        fields = ['id','title','author','isbn','available','price','url']        

    # def get_url(self,obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None

    #     return reverse("product-detail",kwargs={"slug":obj.slug},request= request)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        
