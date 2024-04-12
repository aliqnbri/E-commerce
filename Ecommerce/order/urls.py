from django.urls import path
from order.views import CartViewSet ,OrderCreateAPIView

app_name = 'order'


urlpatterns = [
    # path('', CartAPIView.as_view(),),
    path('create_order/', OrderCreateAPIView.as_view()),
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart_list'),
    path('cart/add/<int:product_id>/', CartViewSet.as_view({'post': 'cart_add'}), name='cart_add'),
    path('cart/remove/<int:product_id>/', CartViewSet.as_view({'post': 'cart_remove'}), name='cart_remove'),
]
#     path('add/<int:product_id>/', views.cart_add, name='cart_add'),
#     path('remove/<int:product_id>/', views.cart_remove,name='cart_remove'),
#     path('create/', views.order_create, name='order_create'),
#     path('admin/order/<int:order_id>/', views.admin_order_detail,name='admin_order_detail'),
#     path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),

# urlpatterns = [
#     path('')
# ]
