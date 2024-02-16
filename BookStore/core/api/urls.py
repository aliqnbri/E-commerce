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

    #<==Account API ==>
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.LoginView.as_view(), name='auth_login'),
    # path('register/',views.RegisterAPI.as_view()),
    # path('login/',views.LoginAPI.as_view()),
     #<==product API ==>
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('product_search/', views.ProductSearch.as_view(), name='product_search'),
    path('product_search/', views.ProductSearch.as_view(), name='product_search'),
    path('coupons/', views.CouponListAPIView.as_view(), name='coupon-list'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    ]



