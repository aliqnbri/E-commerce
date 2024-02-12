from django.urls import path
from product import views

urlpatterns = [
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-list'),
    # path('<slug:slug>/', views.ProductListView.as_view(), name='product-list'),

]
