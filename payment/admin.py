from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Payment, Transaction

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('customer__username', 'order__order_number')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ( 'payment', 'name', 'city', 'state')
    list_filter = ('state',)
    search_fields = ('customer__username', 'name', 'city')