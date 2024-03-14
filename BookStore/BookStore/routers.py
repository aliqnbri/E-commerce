from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category',views.CategoryViewSet())