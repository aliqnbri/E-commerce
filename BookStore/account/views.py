from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from account.forms import LoginForm, UserRegistrationForm, \
                   UserEditForm

from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from core.api.serializers import MyTokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from account import emails ,authentications
from django.views.generic import ListView
from account.models import  CustomUser
from django.shortcuts import render
from django.middleware import csrf
from django.utils import timezone
from rest_framework import status
from django.conf import settings

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
    permission_classes = [AllowAny,]
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





































def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    # Display all actions by default
    
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            username =user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            new_user = CustomUser.objects.create_user(username=username, email=email, password=password)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


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