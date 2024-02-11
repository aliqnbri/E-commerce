from django.contrib import admin
from django.urls import path ,include
from account import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', include('account.urls')),
    # path('account/', include('account.urls')),
    path('api/', include('product.urls')),
    path('product/', include('product.urls')),
    
]
