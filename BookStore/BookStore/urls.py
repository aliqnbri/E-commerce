from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', include('core.api.urls')),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('account/', include('account.urls')),
    path('product/', include('product.urls',namespace='product')),
    path('order/', include('order.urls', namespace='orders')),
    path('cart/', include('order.urls', namespace='cart')),
    path('coupon/', include('coupon.urls', namespace='coupons')),
    path('payment/', include('payment.urls', namespace='payment')),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)