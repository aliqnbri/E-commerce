from django.core.mail import send_mail
from account.models import CustomUser
import string ,random, time, redis
from django.conf import settings
from celery import shared_task
from typing import Any



@shared_task
def send_otp(email: str) -> None:
    """
    Function to send an OTP (One Time Password) to the provided email address.

    Args:
        email (str): The email address to which the OTP will be sent.

    Returns:
        None
    """
    subject: str = 'Your Account Verification'
    otp: str = ''.join(random.choices(string.digits, k=6)) # Generate a 6-digit OTP
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.setex(email, 120, otp)  # Set the OTP with a 2-minute expiration (120 seconds)

    message: str = f'Your verification OTP is: {otp}'
    email_from: str = settings.EMAIL_HOST

    # Sending the OTP email
    send_mail(subject, message, email_from, [email],fail_silently=False)

    # Updating the OTP for the CustomUser with the provided email
    # CustomUser.objects.filter(email=email).update(otp=otp)












