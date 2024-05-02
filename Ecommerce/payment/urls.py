from django.urls import path
from payment import views ,webhooks


app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', webhooks.zarinpal_webhook, name='zarinpal-webhook'),
]