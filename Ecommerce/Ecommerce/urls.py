from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from django.views.generic import TemplateView



urlpatterns = [
    # path('', include('home.urls')),
    # path('', TemplateView.as_view(template_name='index.html')),
    path('api/schema/',SpectacularAPIView.as_view() ,name='schema'),
    path('api/schema/docs/',SpectacularSwaggerView.as_view(url_name='schema') ),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('product/', include('product.routers', namespace='product')),
    path('order/', include('order.urls', namespace='orders')),
    # path('cart/', include('order.urls', namespace='cart')),
    # path('coupon/', include('coupon.urls', namespace='coupons')),
    # path('payment/', include('payment.urls', namespace='payment')),
    # path('__debug__/', include('debug_toolbar.urls')),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)