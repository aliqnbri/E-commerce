from rest_framework import viewsets
from product.models import Product ,Category
from product.serializers import ProductSerializer ,CategorySerializer
from rest_framework.response import Response


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

    def list(self,request):
        serilizer = self.serializer_class(self.queryset, many=True)

        return Response(serilizer.data)





class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
