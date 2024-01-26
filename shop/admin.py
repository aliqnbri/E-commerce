from django.contrib import admin

# Register your models here.
from .models import Category, Product


# @admin.register(Product)
class ProductsInline(admin.TabularInline):
    model = Product
    extra = 3  # Add three more products per category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'products_count',  # Added field to display product count
       
    ]
    list_filter = ['name']
   
    ordering = ['name']
    # Added field to search by description
    search_fields = ['name',]
    inlines = [ProductsInline]  # Added inline admin form for managing products
    fields = ['name', 'slug',]  # Reordered fields
    def products_count(self, obj):
        return obj.products.count()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'category',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    list_per_page = 10  # Set pagination to 10 items per page
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created', 'updated']
    # Added custom actions
    actions = ['mark_as_unavailable', 'restore_availability']

    def mark_as_unavailable(self, request, queryset):
        for obj in queryset.filter(available=True):
            obj.available = False
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products marked as unavailable')

    def restore_availability(self, request, queryset):
        for obj in queryset.filter(available=False):
            obj.available = True
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products restored to availability')

    mark_as_unavailable.short_description = 'Mark as unavailable'
    restore_availability.short_description = 'Restore availability'

    




# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
