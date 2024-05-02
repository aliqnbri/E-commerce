from rest_framework.routers import DefaultRouter
from product.viewset import  CategoryViewSet ,ProductViewSet
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

app_name = 'product'




router = DefaultRouter()
router.register(r'category',CategoryViewSet,basename='category')
router.register(r'product', ProductViewSet, basename='product')


urlpatterns = router.urls