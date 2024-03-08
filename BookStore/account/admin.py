from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from account.forms import UserAdminCreationForm, UserAdminChangeForm
from core.managers import export_to_csv
from typing import List, Tuple

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    The forms to add and change user instances
    """
    form: Type[UserAdminChangeForm] = UserAdminChangeForm
    add_form: Type[UserAdminCreationForm] = UserAdminCreationForm

    list_display: List[str] = ['username', 'email', 'role']
    list_filter: List[str] = ['role']
    fieldsets: Tuple[Tuple[str, dict], Tuple[str, dict], Tuple[str, dict]] = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'role')}),
    )

    add_fieldsets: Tuple[Tuple[str, dict]] = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
         ),
    )
    search_fields: List[str] = ['username', 'email']
    ordering: str = '-created'
    filter_horizontal: Tuple = ()
    actions: List[Callable] = [export_to_csv]

admin.site.register(User, CustomUserAdmin)















class CustomUserAdmin(UserAdmin):
    """
    The forms to add and change user instances
    """
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['username', 'email', 'role',]
    list_filter = ['role']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'role')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
         ),
    )
    search_fields = ['username','email']
    ordering = ['-created']
    filter_horizontal = ()
    actions = [export_to_csv]


admin.site.register(User, CustomUserAdmin)
