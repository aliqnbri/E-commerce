from django.urls import path
from order.api import views


app_name = 'order'


urlpatterns = [
    path('', views.CartAPIView.as_view(),),
#     path('add/<int:product_id>/', views.cart_add, name='cart_add'),
#     path('remove/<int:product_id>/', views.cart_remove,name='cart_remove'),
#     path('create/', views.order_create, name='order_create'),
#     path('admin/order/<int:order_id>/', views.admin_order_detail,name='admin_order_detail'),
#     path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),
]
# urlpatterns = [
#     path('')
# ]
