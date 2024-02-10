from django.contrib import admin
from django.urls import path ,include
from account import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('product/', include('product.urls')),
    
]
