from django.urls import path
from account import views

urlpatterns = [
    path('api/login/',views.LoginAPI.as_view()),
    path('api/verify/',views.VerifyOTP.as_view()),
]




