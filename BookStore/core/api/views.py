# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework_simplejwt.views import TokenObtainPairView
# from core.api.serializers import MyTokenObtainPairSerializer
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken
# from product.models import Product, Category, Review
# from rest_framework.authtoken.models import Token
# from rest_framework.generics import CreateAPIView
# from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from django.core.paginator import Paginator
# from account import emails ,authentications
# from django.views.generic import ListView
# from rest_framework.views import APIView
# from account.models import  CustomUser
# from django.shortcuts import render
# from django.middleware import csrf
# from django.utils import timezone
# from rest_framework import status
# from django.conf import settings
# from datetime import timedelta
# from core.api import serializers
# from coupon.models import Coupon
# from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny








# class CouponListAPIView(APIView):
#     def get(self, request):
#         coupons = Coupon.objects.all()
#         serializer = serializers.CouponSerializer(coupons, many=True)
#         return Response(serializer.data)

        
    











#   # if not username or not password or not email:
#             #     return Response({'error': 'Please provide username, password and Email'}, status=status.HTTP_400_BAD_REQUEST)

#             # if User.objects.filter(email=email).exists():
#             #     return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#             # if User.objects.filter(username=username).exists():
#             #     return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

#             # user = CustomUser.objects.create_user(username=username, email=email, password=password)
#             # user.save()



