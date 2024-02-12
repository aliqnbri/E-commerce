from django.urls import path
from core.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,

)
urlpatterns = [
    # path('verify/',views.VerifyOTP.as_view()),
    # path('user/',views.UserView.as_view()),
    # path('logout/',views.LogoutView.as_view()),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.LoginView.as_view(), name='auth_login'),
    # path('register/',views.RegisterAPI.as_view()),
    # path('login/',views.LoginAPI.as_view()),
]

