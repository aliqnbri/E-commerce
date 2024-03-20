from rest_framework.routers import DefaultRouter
from product.viewset import ProductViewSet , CategoryViewSet

router = DefaultRouter()
router.register(r'category',CategoryViewSet,basename='category')
router.register(r'product', ProductViewSet, basename='product')


urlpatterns = router.urls