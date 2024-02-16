from account import emails ,authentications
from account.models import  CustomUser
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.views.generic import ListView
from rest_framework.views import APIView
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from rest_framework import status
from django.conf import settings
from datetime import timedelta
from product import models
from core.api import serializers
from coupon.models import Coupon
from product.models import Product, Category, Review





class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RegisterSerializer


class LoginView(APIView):
     def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not username or not password or not email:
            return Response({'error': 'Please provide both username and password and Email'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        user = models.CustomUser.objects.filter(email=email).first()

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
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

        
    
























































# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = serializers.ProductSerializer(data=request.data)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductSearch(APIView):
#     def get(self, request):

#         query = request.GET.get('query')

#         if not query:
#             return Response("Please provide a search query.", status=status.HTTP_400_BAD_REQUEST)

#         """Filter products based on the search query (case-insensitive search in the title field)"""
#         products = Product.objects.filter(title__icontains=query)

#         """Check if any products match the search query"""
#         if not products:
#             return Response("No products found for the search query.", status=status.HTTP_400_BAD_REQUEST)

#         # Serialize the products that match the search query
#         serializer = serializers.ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ReviewList(APIView):
#     def get(self, request):
#         reviews = Review.objects.all()
#         serializer = serializers.ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryList(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = serializers.CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














# class LoginAPI(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = models.CustomUser.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed('User Not Found')
#         # if not user.check_password(password):
#         #     raise AuthenticationFailed('Incorect Password')
#         if user.is_active:
#             pass

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()}

#         token = jwt.encode(payload, 'secret')  # .decode('utf-8')
#         response = Response({'jwt': token})
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         return response

#         return Response({
#             'message': 'Login was successful !'
#         })

#         # if user.is_verified is False:
#         #     return Response({
#         #         'status': status.HTTP_400_BAD_REQUEST,
#         #         'message': 'your account is not verified',
#         #         'data': serializer.errors
#         #     })

#         # return Response({
#         #     'status': status.HTTP_400_BAD_REQUEST,
#         #     'message': 'Sth went Wrong',
#         #     'data': serializer.errors
#         # })


# class RegisterAPI(APIView):
#     def post(self, request):
#         serializer = serializers.UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({
#                 'status': status.HTTP_200_OK,
#                 'message': 'Registeration Successfuly check Email',
#                 'data': serializer.errors
#             })
#         return Response({
#             'status': status.HTTP_400_BAD_REQUEST,
#             'message': 'Sth went Wrong',
#             'data': serializer.errors
#         })


# class VerifyOTP (APIView):
#     def post(self, request):

#         data = request.data
#         serializer = serializers.VerifyAccountSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data['email']
#             otp = serializer.data['otp']
#             if not (user := CutomUser.objects.filter(email=email).exists()):
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'somethin went wrong',
#                     'data': 'Invalid Emil',
#                 })
#             if user[0].otp != otp:
#                 return Response({
#                     'status': status.HTTP_200_OK,
#                     'message': 'Verified !',
#                     'data': {},
#                 })

#         return Response({
#             'status': status.HTTP_400_BAD_REQUEST,
#             'message': 'Sth went Wrong',
#             'data': serializer.errors
#         })


# class UserView(APIView):
#     def get(self, request):
#         try:
#             token = request.COOKIES.get('jwt')

#             if not token:
#                 raise AuthenticationFailed('Token missing')
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#             user = models.CustomUser.objects.filter(id=payload['id']).first()
#             if not user:
#                 raise AuthenticationFailed('User not found.')
#             serializer = serializers.UserSerializer(user)

#             return Response(serializer.data)

#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired. Please log in again.')

#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token. Please log in again.')

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     def post(self,request):
#         response = Response(data={'message' : 'success'})
#         response.delete_cookie('jwt')
#         return response
# from account import serializers, models, emails ,authentications
# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.generics import CreateAPIView
# from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from django.shortcuts import render
# from django.middleware import csrf
# from django.utils import timezone
# from rest_framework import status
# from django.conf import settings
# from datetime import timedelta


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = serializers.MyTokenObtainPairSerializer

# class RegisterView(CreateAPIView):
#     queryset = models.CustomUser.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = serializers.RegisterSerializer



# class LoginView(APIView):
#      def post(self, request):
#         data = request.data
#         email = data.get('email')
#         username = data.get('username')
#         password = data.get('password')

#         if not username or not password or not email:
#             return Response({'error': 'Please provide both username and password and Email'}, status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(username=username, password=password)
#         user = models.CustomUser.objects.filter(email=email).first()

#         if user is not None and user.is_active:
#             tokens = authentications.get_tokens_for_user(user)
#             token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
#             iran_delta = timedelta(hours=3, minutes=30)
            
#             response = Response({"message": "Login successful", "data": tokens})
#             response.set_cookie(
#                 key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#                 value=tokens["access"],
#                 max_age=iran_delta + token_lifetime,
#                 secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                 httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                 samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#             )
#             csrf.get_token(request)
#             return response
#         elif user is None:
#             return Response({"error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"error": "This account is not active"}, status=status.HTTP_404_NOT_FOUND)
































# class LoginAPI(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = models.CustomUser.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed('User Not Found')
#         # if not user.check_password(password):
#         #     raise AuthenticationFailed('Incorect Password')
#         if user.is_active:
#             pass

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()}

#         token = jwt.encode(payload, 'secret')  # .decode('utf-8')
#         response = Response({'jwt': token})
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         return response

#         return Response({
#             'message': 'Login was successful !'
#         })

#         # if user.is_verified is False:
#         #     return Response({
#         #         'status': status.HTTP_400_BAD_REQUEST,
#         #         'message': 'your account is not verified',
#         #         'data': serializer.errors
#         #     })

#         # return Response({
#         #     'status': status.HTTP_400_BAD_REQUEST,
#         #     'message': 'Sth went Wrong',
#         #     'data': serializer.errors
#         # })


# class RegisterAPI(APIView):
#     def post(self, request):
#         serializer = serializers.UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({
#                 'status': status.HTTP_200_OK,
#                 'message': 'Registeration Successfuly check Email',
#                 'data': serializer.errors
#             })
#         return Response({
#             'status': status.HTTP_400_BAD_REQUEST,
#             'message': 'Sth went Wrong',
#             'data': serializer.errors
#         })


# class VerifyOTP (APIView):
#     def post(self, request):

#         data = request.data
#         serializer = serializers.VerifyAccountSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data['email']
#             otp = serializer.data['otp']
#             if not (user := CutomUser.objects.filter(email=email).exists()):
#                 return Response({
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'somethin went wrong',
#                     'data': 'Invalid Emil',
#                 })
#             if user[0].otp != otp:
#                 return Response({
#                     'status': status.HTTP_200_OK,
#                     'message': 'Verified !',
#                     'data': {},
#                 })

#         return Response({
#             'status': status.HTTP_400_BAD_REQUEST,
#             'message': 'Sth went Wrong',
#             'data': serializer.errors
#         })


# class UserView(APIView):
#     def get(self, request):
#         try:
#             token = request.COOKIES.get('jwt')

#             if not token:
#                 raise AuthenticationFailed('Token missing')
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#             user = models.CustomUser.objects.filter(id=payload['id']).first()
#             if not user:
#                 raise AuthenticationFailed('User not found.')
#             serializer = serializers.UserSerializer(user)

#             return Response(serializer.data)

#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired. Please log in again.')

#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token. Please log in again.')

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     def post(self,request):
#         response = Response(data={'message' : 'success'})
#         response.delete_cookie('jwt')
#         return response
