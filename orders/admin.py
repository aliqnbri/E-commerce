from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]