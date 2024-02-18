from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from core.api.serializers import MyTokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from product.models import Product, Category, Review
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from account import emails ,authentications
from django.views.generic import ListView
from rest_framework.views import APIView
from account.models import  CustomUser
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from rest_framework import status
from django.conf import settings
from datetime import timedelta
from core.api import serializers
from coupon.models import Coupon




class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


#it was (CreateAPIView)
class RegisterView(APIView):
    permission_classes = [AllowAny]
    # queryset = CustomUser.objects.all()
    # permission_classes = (IsAuthenticated,)
    # serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user :
                # return Response(status=status.HTTP_201_CREATED)
          
                # token = Token.objects.get_or_create(user=user)
                # Assuming 'user' is the user object for which you want to create a token
                token, created = Token.objects.get_or_create(user=user)

                # token = Token.objects.create(user=user)
                token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                iran_delta = timedelta(hours=3, minutes=30)
                response = Response({"message": "Register successful", "data": {'token': token.key}})
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token.key,
                    max_age=iran_delta + token_lifetime,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                return response






class RegisterAPI(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Registeration Successfuly check Email',
                'data': serializer.errors
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Sth went Wrong',
            'data': serializer.errors
        })


class LoginView(APIView):
     def post(self, request):
        data = request.data
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password or not email:
            return Response({'error': 'Please provide username, password and Email'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, username=username,password=password)
        user = CustomUser.objects.filter(email=email).first()

        if user is not None and user.is_active:
            tokens = authentications.get_tokens_for_user(user)
            token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            iran_delta = timedelta(hours=3, minutes=30)
            
            response = Response({"message": "Login successful", "data": tokens})
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=tokens["access"],
                max_age=iran_delta + token_lifetime,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            csrf.get_token(request)
            return response
        elif user is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "This account is not active"}, status=status.HTTP_404_NOT_FOUND)



class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProductSearch(APIView):
    def get(self, request):    
        products = Product.objects.all()
        query = request.GET.get('query')

        if not query:
            return Response("Please provide a search query.", status=status.HTTP_400_BAD_REQUEST)

        """Filter products based on the search query (case-insensitive search in the title field)"""
        products = models.Product.objects.filter(title__icontains=query)

        """Check if any products match the search query"""
        if not products:
            return Response("No products found for the search query.", status=status.HTTP_400_BAD_REQUEST)

        # Serialize the products that match the search query
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewList(APIView):
    def get(self, request):
        reviews = models.Review.objects.all()
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
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CouponListAPIView(APIView):
    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = serializers.CouponSerializer(coupons, many=True)
        return Response(serializer.data)

        
    











  # if not username or not password or not email:
            #     return Response({'error': 'Please provide username, password and Email'}, status=status.HTTP_400_BAD_REQUEST)

            # if User.objects.filter(email=email).exists():
            #     return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            # if User.objects.filter(username=username).exists():
            #     return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # user = CustomUser.objects.create_user(username=username, email=email, password=password)
            # user.save()



