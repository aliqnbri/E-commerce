from django.core.mail import send_mail
import random
from django.conf import settings
from account.models import CustomUser



def send_otp(email):
    subject = 'Your Account Verification Email'
    otp = random.randint(1000, 999999)
    message = f'Your OTP is: {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    CustomUser.objects.filter(email=email).update(otp=otp)