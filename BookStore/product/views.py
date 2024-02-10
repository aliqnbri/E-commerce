from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from product import serializers
from django.views.generic import ListView


class ProductListView(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 2
    queryset = Product.objects.all()
    # def get_queryset(self):
    #     return Product.objects.all()



class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(data=request.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSearch(APIView):
    def get(self, request):

        query = request.GET.get('query')

        if not query:
            return Response("Please provide a search query.", status=status.HTTP_400_BAD_REQUEST)

        """Filter products based on the search query (case-insensitive search in the title field)"""
        products = Product.objects.filter(title__icontains=query)

        """Check if any products match the search query"""
        if not products:
            return Response("No products found for the search query.", status=status.HTTP_400_BAD_REQUEST)

        # Serialize the products that match the search query
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewList(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
