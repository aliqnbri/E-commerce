from django.contrib import admin
from .models import Category, Author, Book

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'description',  # Added field to display description
        'books_count',  # Added field to display book count
    ]
    list_filter = ['name']
    # readonly_fields = ['created', 'updated']  # Added to hide fields from edit
    ordering = ['name']
    search_fields = ['name',]  # Added field to search by description
    fields = ['name', 'slug', 'description']  # Reordered fields
    prepopulated_fields = {'slug': ('name',)}

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = 'Number of Books'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'slug',
        'bio',
    ]
    # Added filter for first and last names
    list_filter = ['first_name', 'last_name']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    search_fields = ['first_name', 'last_name',]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'slug',
        'author',
        'isbn',
        'price',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['available', 'created', 'updated', 'author']
    list_editable = ['price', 'available',]
    list_per_page = 10  # Set pagination to 10 items per page
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created', 'updated']
    # Added custom actions
    actions = ['mark_as_unavailable', 'restore_availability']

    def mark_as_unavailable(self, request, queryset):
        for obj in queryset.filter(available=True):
            obj.available = False
            obj.save()
        self.message_user(
            request, f'{queryset.count()} books marked as unavailable')

    def restore_availability(self, request, queryset):
        for obj in queryset.filter(available=False):
            obj.available = True
            obj.save()
        self.message_user(
            request, f'{queryset.count()} books restored to availability')

    mark_as_unavailable.short_description = 'Mark as unavailable'
    restore_availability.short_description = 'Restore availability'
