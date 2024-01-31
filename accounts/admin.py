from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .forms import RegisterForm,UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.



User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'role']
    list_filter = ['role']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active','role')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password','password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)




