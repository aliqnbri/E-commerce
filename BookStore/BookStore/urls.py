from django.contrib import admin
from django.urls import path ,include
from account import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('login/',views.LoginAPI.as_view()),
    path('verify/',views.VerifyOTP.as_view()),
]
