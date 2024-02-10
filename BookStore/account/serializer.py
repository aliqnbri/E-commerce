from rest_framework import serializers
from .models import CustomUser, CustomerProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"


class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
