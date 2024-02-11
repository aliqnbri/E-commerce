from django.core.mail import send_mail
import random
from django.conf import settings
from account.models import CustomUser


def sent_otp (email):
    subject = 'Your account Verification Email'
    otp = random.randint(1000,999999)
    message = f' your OTP is : {otp}'
    email_from = settings.EMAIL_HOST
    send_mail (subject , message, email_from , [email])
    user_obj = CustomUser.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()