from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import emails, authentications
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import CustomUser
from account import serializers
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from rest_framework.generics import GenericAPIView
from account.utils.emails import send_otp ,check_otp
from Ecommerce.redis_cllient import redis_client




class RegisterUserView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            email = user_data['email']
            # send verification mail to the registered user
            send_otp(email=email)

            return Response({"message": f"register successful \n OTP code sent to {email}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer




class VerifyOtp(GenericAPIView):
    serializer_class = serializers.VerifyOtpSerialiser
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        data = request.data
        email = data['email']
        otp = send_otp(email) 
        return Response({"data": {email: otp}})

    def get(self,request):
        data = request.data
        email = data['email']
        stored_otp = cache.get(email)
        if not stored_otp:
            raise serializers.ValidationError("OTP has expired or invalid")

        if check_otp(email=email,otp=stored_otp):
            


            return Response({"data":otp })    




















  # response_data = {
        #     "message": f"Register successful an Verfication code sent to {user.email}",
        #     "data": {
        #         "refresh": str(refresh),  # Return refresh token
        #         "access": str(access)  # Return access token
        #     }
        # }






            
            # token, created = Token.objects.get_or_create(user=user)

            # token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            # iran_delta = timedelta(hours=3, minutes=30)
            # new_lifetime = token_lifetime + iran_delta
            # token.lifetime = new_lifetime
            # token.save()
            
        #     response_data = {
        #         "message": "Register successful",
        #         "data": {
        #             "token": str(token)
        #         }
        #     }

        #     response = Response(data=response_data, status=status.HTTP_201_CREATED)
        #     response.set_cookie(
        #         key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        #         value=token.key,
        #         max_age=iran_delta + token_lifetime,
        #         secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #         httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        #         samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        #     )
        #     return response
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















# class LoginView(APIView):
#     # permission_classes = [permissions.AllowAny]
#     authentication_classes = [authentications.CustomAuthentication]
#     serializer_class = serializers.LoginSerializer

#     def post(self, request):
#         data = request.data
#         email = data.get('email')
#         password = data.get('password')
#         if self.serializer_class.is_valid(raise_exception=True):

#             tokens, created = authentications.get_tokens_for_user(user)
#             token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
#             iran_delta = timedelta(hours=3, minutes=30)
#             data = {"message": "Login successful", "data": tokens}
#             response = Response(data=data, status=status.HTTP_200_OK)
#             response.set_cookie(
#                 key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#                 value=tokens['access'],
#                 max_age=iran_delta + token_lifetime,
#                 secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                 httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                 samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#             )
#             csrf.get_token(request)
#             return response
#         Response(status=status.HTTP_404_NOT_FOUND)






# class RegisterCreateAPIView(CreateAPIView):
#     """
#     API view for user registration.
#     """
#     permission_classes = [permissions.AllowAny]
#     serializer_class = serializers.RegisterSerializer

#     def perform_create(self, serializer):
#         """
#         Perform custom actions after creating a new user instance.
#         """
#         user = serializer.save()
#         # Generate refresh and access tokens
#         refresh = RefreshToken.for_user(user)
#         access = refresh.access_token
#         print(f"acceess is {access}")
#         # Adjust expiration for Iran's time zone
#         access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
#         iran_delta = timedelta(hours=3, minutes=30)
#         response = Response({"message": f"Register successful an Verfication code sent to {user.email}"}, status=status.HTTP_201_CREATED)
#         response.set_cookie(
#             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#             value=str(access),
#             expires=access_lifetime + iran_delta,
#             httponly=True,
#             secure=False,  # Enforce HTTPS
#         )

#         return response

