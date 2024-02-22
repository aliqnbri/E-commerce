from django.contrib import admin
from core.managers import export_to_csv
from .models import Order, OrderItem




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer',
                    'created', 'updated']
    list_filter = ['created', 'updated',]
    inlines = [OrderItemInline]
    actions = [export_to_csv]