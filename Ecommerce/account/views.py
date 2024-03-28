from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import emails ,authentications
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token

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

#         return Response(status=status.HTTP_204_NO_CONTEN)


class RegisterCreateAPIView(CreateAPIView):
    """
    API view for user registration.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer
 


    def perform_create(self,serializer):
        """
        Perform custom actions after creating a new user instance.
        """
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                token,created = Token.objects.get_or_create(user=user)
    
                token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                iran_delta = timedelta(hours=3, minutes=30)
                new_lifetime = token_lifetime + iran_delta
                token.lifetime = new_lifetime
                token.save()
            
                response_data = {
                    "message": "Register successful",
                    "data": {
                        "token": token.key
                    }
                }


                response = Response(response_data,status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token.key,
                    max_age=iran_delta + token_lifetime,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            return response


class LoginView(APIView):
    # permission_classes = [permissions.AllowAny]
    authentication_classes = [authentications.CustomAuthentication]
    serializer_class = serializers.LoginSerializer
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if self.serializer_class.is_valid(raise_exception=True):

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
        Response(status=status.HTTP_404_NOT_FOUND)    





