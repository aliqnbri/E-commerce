from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'product', 'discount_percent', 'discount_amount', 'expiration_date', 'valid_from', 'is_active']
    list_filter = ['is_active', 'valid_from', 'expiration_date', 'product']
    search_fields = ['code', 'product']



