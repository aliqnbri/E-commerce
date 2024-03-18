from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path, include
from account import views

app_name = 'account'
urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.RegisterCreateAPIView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]







