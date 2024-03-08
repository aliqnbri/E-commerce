from rest_framework import viewsets
from product.models import Product
from product.serializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> queryset
    get -> retrive -> product instance Detail View
    post -> create -> new instance
    put -> Update
    delete -> Destroy
    '''
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
