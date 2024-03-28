from rest_framework import viewsets
from product.serializers import ProductSerializer ,CategorySerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from product.models import Product ,Category
from rest_framework.viewsets import ViewSet



class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @extend_schema(responses=serializer_class)
    def list(self,request):
        serilizer = self.serializer_class(self.queryset, many=True)

        return Response(serilizer.data)




class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


    @extend_schema(responses=serializer_class)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def retrieve(self, request, slug=None):
        product = get_object_or_404(self.queryset, slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(responses=serializer_class)
    def update(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


    @extend_schema(responses=serializer_class)
    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()
        return Response({'message': 'Product deleted'})



