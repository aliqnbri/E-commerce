from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializer import LoginSerailizer, VerifyAccountSerializer, UserSerializer


class LoginAPI(APIView):
    def psot(self, request):
        try:
            data = request.data
            serializer = LoginSerailizer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email, password=password)

                if user is None:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid Password',
                        'data': {}})

                if user.is_verified is False:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'your account is not verified',
                        'data': serializer.errors
                    })

                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Sth went Wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
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

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An error occurred during registration.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTP (APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = CutomUser.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'somethin went wrong',
                        'data': 'Invalid Emil',
                    })
                if user[0].otp != otp:
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'Verified !',
                        'data': {},
                    })

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Sth went Wrong',
                'data': serializer.errors
            })

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An error occurred during verifiy.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
