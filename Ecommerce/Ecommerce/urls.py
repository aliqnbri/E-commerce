from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from .routers import router
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('api/', include('Ecommerce.routers')),
    # path('product/', include('product.urls',namespace='produ')),
    # path('order/', include('order.urls', namespace='orders')),
    # path('cart/', include('order.urls', namespace='cart')),
    # path('coupon/', include('coupon.urls', namespace='coupons')),
    # path('payment/', include('payment.urls', namespace='payment')),
    # path('__debug__/', include('debug_toolbar.urls')),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)