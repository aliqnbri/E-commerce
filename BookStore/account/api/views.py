from account.api import serializers
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
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer


class RegisterCreateAPIView(CreateAPIView):
    """
    API view for user registration.
    """
    # authentication_classes = [authentications.CustomAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer
    queryset = CustomUser.objects.all()
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
                token = Token.objects.get_or_create(user=user)
    
                token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                iran_delta = timedelta(hours=3, minutes=30)
                data = {"message": "Register successful", "data" : {'token': token[0]}}
                response = Response(data=data,status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token[0],
                    max_age=iran_delta + token_lifetime,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            return response


class LoginView(APIView):
    parser_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentications.CustomAuthentication]
    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not username or not password or not email:
            return Response({'error': 'Please provide username, password and Email'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(email=email).first()

        if user is not None and user.is_active:
            tokens = authentications.get_tokens_for_user(user)
            token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            iran_delta = timedelta(hours=3, minutes=30)
            data = {"message": "Login successful", "data": tokens}
            response = Response(data=data,status=status.HTTP_200_OK)
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




@login_required
def dashboard(request):

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})




@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})