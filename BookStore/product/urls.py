from django.urls import path
from product import views

app_name = 'product'

#     path('', views.product_list, name='product_list'),
#     path('<slug:category_slug>/', views.product_list,
#          name='product_list_by_category'),
#     path('<int:id>/<slug:slug>/', views.product_detail,
#          name='product_detail'),
# ]


urlpatterns = [

#                         <== Product API ==>
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', views.ProductDetailAPIView.as_view(), name='product_list'),
    path('product_search/', views.ProductSearch.as_view(), name='product_search'),
    path('category/', views.CategoryList.as_view(), name='category-list'),


]