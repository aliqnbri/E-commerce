from django.contrib import admin

# Register your models here.
# from .models import BaseModel


# @admin.register(BaseModel)
# class BaseModelAdmin(admin.ModelAdmin):
#     list_display = ('id', 'created', 'updated', 'is_deleted')
#     list_filter = ('is_deleted',)

#     def get_fields(self, request, obj=None):
#         fields = super().get_fields(request, obj)

#         if obj is not None and obj.is_deleted:
#             fields = [f for f in fields if f.name != 'delete']

#         return fields

#     def delete_model(self, request, obj):
#         if not obj.is_deleted:
#             obj.is_deleted = True
#             obj.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return HttpResponseForbidden('Object is already deleted')

#     delete_model.allowed_methods = ('post',)
