from rest_framework.routers import DefaultRouter
from product.viewset import ProductViewSet

router = DefaultRouter()
router.register(r'category',views.CategoryViewSet(),basename='category')
router.register(r'product', ProductViewSet, basename='product')


urlpatterns = router.urls