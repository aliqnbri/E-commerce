from django.shortcuts import render
from home.models import ShopInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from product.models import Product



def index_view(request):
    return render(request, 'home/index.html')
