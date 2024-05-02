from django.core.mail import send_mail
import string ,random ,time
from django.conf import settings
from celery import shared_task
from typing import Any
from Ecommerce.redis_cllient import redis_client
cache = redis_client()


# @shared_task
def send_otp(email: str) -> None:
    """
    Function to send an OTP (One Time Password) to the provided email address.
    """
    subject: str = 'Register Verification'
    otp: str = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
    print(otp)

    # Cache the OTP and its expiration time (2 minutes)
    cache = redis_client()
    cache.set(email, otp, ex=120)
    

    message: str = f'Your verification OTP is: {otp}'
    email_from: str = settings.EMAIL_HOST

    # Sending the OTP email
    send_mail(subject, message, email_from, [email], fail_silently=False)

    return otp


def check_otp(email: str, otp: str) -> bool:

    cached_otp = cache.get(email)
    
    if cached_otp is None:
        raise ValueError ("OTP has not been sent or has expired")
    
    if cached_otp == otp:
        cache.delete(email)
        return True
    return False











# class OTPSingleton:
#     _instance = None
#     _redis_client = None

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._redis_client = redis.Redis(host='localhost', port=6379, db=0)
#         return cls._instance

#     def generate_otp(self, phone_number):
#         otp = ''.join(random.choices('0123456789', k=6))
#         self._redis_client.setex(phone_number, time=300, value=otp)
#         return otp

#     def validate_otp(self, phone_number, user_input_otp):
#         stored_otp = self._redis_client.get(phone_number)
#         if stored_otp is None:
#             return False
#         else:
#             correct_otp = stored_otp.decode('utf-8')
#             self._redis_client.delete(phone_number)
#             return user_input_otp == correct_otp











# import random
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username', 'first_name', 'last_name')

# class OTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         user = User.objects.filter(email=value).first()
#         if not user:
#             user = User.objects.create(
#                 username="Username",
#                 email=value,
#             )
#             user.save()
#         self.user = user
#         return value

#     def generate_otp(self):
#         return random.randint(100000, 999999)

#     def save(self):
#         otp = self.generate_otp()
#         cache_key = f"otp:{self.user.email}"
#         redis_client = get_redis_connection("default")
#         redis_client.setex(cache_key, 120, otp)
#         return self.user

# class CompleteRegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField()

#     def validate_otp(self, value):
#         cache_key = f"otp:{self.initial_data['email']}"
#         redis_client = get_redis_connection("default")
#         stored_otp = redis_client.get(cache_key)
#         if not stored_otp:
#             raise serializers.ValidationError("OTP has expired or invalid")

#         if int(value) != int(stored_otp.decode()):
#             raise serializers.ValidationError("Invalid OTP")

#         # Delete the OTP from the cache
#         redis_client.delete(cache_key)

#         return value

#     def save(self, *args, **kwargs):
#         user = self.user
#         user.set_password(self.initial_data['password'])
#         user.save()
#         return user