from django.urls import path
from product import views

app_name = 'product'

urlpatterns = [
#                         <== Product API ==>

    # path('', views.ProductListCreateAPIView.as_view(), name='product'),
    # path('', views.ProductMixinVeiw.as_view(), name='product_list'),
    path('', views.ProductCreateAPIView.as_view(), name='product_list'),
    path('create/', views.ProductCreateAPIView.as_view(), name='product_list'),
    # path('<slug:slug>/', views.ProductDetailAPIView.as_view(), name='product_list'),
    path('<slug:slug>/', views.ProductMixinVeiw.as_view(), name='product_detail'),
    path('update/<slug:slug>/', views.ProductUpdateAPIView.as_view()),
    path('delete/<slug:slug>/', views.ProductDeleteAPIView.as_view()),




    # # path('product_list/', views.ProductListView.as_view(), name='product_list'),
    # path('product_search/', views.ProductSearch.as_view(), name='product_search'),
    # path('category/', views.CategoryList.as_view(), name='category-list'),


]