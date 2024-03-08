from django.core.mail import send_mail
from account.models import CustomUser
from django.conf import settings
from typing import Any
import random


def send_otp(email: str) -> None:
    """
    Function to send an OTP (One Time Password) to the provided email address.

    Args:
        email (str): The email address to which the OTP will be sent.

    Returns:
        None
    """
    subject: str = 'Your Account Verification Email'
    otp: int = random.randint(1000, 999999)
    message: str = f'Your OTP is: {otp}'
    email_from: str = settings.EMAIL_HOST

    # Sending the OTP email
    send_mail(subject, message, email_from, [email])

    # Updating the OTP for the CustomUser with the provided email
    CustomUser.objects.filter(email=email).update(otp=otp)
