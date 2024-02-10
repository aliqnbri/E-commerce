from django.urls import path
from product import views

urlpatterns = [
    path('api/categories/', views.CategoryList.as_view(), name='category-list'),
    path('api/products/', views.ProductList.as_view(), name='product-list_view'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('api/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('api/search/', views.ProductSearch.as_view(), name='product-search'),
]
