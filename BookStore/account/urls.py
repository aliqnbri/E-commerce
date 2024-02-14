from django.urls import path
from account import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('dashboard/', views.RegisterView.as_view(), name='auth_register'),
    # path('logout/',views.LogoutView.as_view()),
    # path('verify/',views.VerifyOTP.as_view()),
    # path('user/',views.UserView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('login/', views.LoginView.as_view(), name='auth_login'),
    # path('register/',views.RegisterAPI.as_view()),
]








