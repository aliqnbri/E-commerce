from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from product import serializers
from django.views.generic import ListView
from django.core.paginator import Paginator


class ProductListView(ListView):
    """
    List of products 
    """
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        """queryset to include only available products"""
        queryset = Product.objects.filter(available=True).order_by('-created')
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """queryset to include only available products"""
        queryset = Product.objects.filter(available=True).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object(queryset=get_queryset())

        reviews = Review.objects.filter(product=product)

        context['reviews'] = reviews

        return context

    def get_object(self, queryset=None):
        """Get the product object based on the slug field"""
        slug = self.kwargs.get('slug')
        obj = Product.objects.get(slug=slug)
        return obj
