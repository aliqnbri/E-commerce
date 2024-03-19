from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import emails ,authentications
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import CustomUser
from account import serializers
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer 



# class GenerateOTP(generics.CreateAPIView):
#     serializer_class = OTPSerializer
#     throttle_classes = [AnonRateThrottle]

#     def post(self, request, *args, **kwargs):
#         if request.data.get('phone'):
#             otp = otp_generator(10000, 99999)
#             cache.set(request.data['phone'], otp, 60 * 2)

#         else:
#             data = {"error": "phone field required"}
#             return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

#         send_sms_to_user.delay(request.data['phone'], otp)

#         return Response(status=status.HTTP_204_NO_CONTENT)











class RegisterAPIView(APIView):
    def post(self,request):
        serializer = serializers.RegisterSerializer(data=request.Post)
        if serializer.is_valid(raise_exception=True):
            CustomUser.objects._create_user(
                email=serializer.validated_data['email'],
                phone_number= serializer.validated_data['phone_number'],
                password=serializer.validated_data['password']
            )
            return Response(serializer.data)
        return Response (serializer.errors)


class RegisterCreateAPIView(CreateAPIView):
    """
    API view for user registration.
    """
  
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer
    def perform_create(self,serializer):
        """
        Perform custom actions after creating a new user instance.

        Args:
            serializer: The serializer instance used for user registration.

        Returns:
            Response: The response object with registration status and token information.
        """
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                token,created = Token.objects.get_or_create(user=user)
    
                token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                iran_delta = timedelta(hours=3, minutes=30)
                # data = {'token': token}
                response = Response({"message": "Register successful", "data" : {'token': token}},status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token,
                    max_age=iran_delta + token_lifetime,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            return response


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentications.CustomAuthentication]
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not password or not email:
            return Response({'error': 'Please provide password and Email'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(email=email,password=password).first()
  

        if user is not None and user.is_active:
            tokens,created = authentications.get_tokens_for_user(user)
            token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            iran_delta = timedelta(hours=3, minutes=30)
            data = {"message": "Login successful", "data": tokens}
            response = Response(data=data,status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=tokens['access'],
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





