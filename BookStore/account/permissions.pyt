from rest_framework import permissions


class IsSaffEditorPermission(permissions.DjangoModelPermissions):
    def has_permission(self,request,view):
        user = request.user
        if user.is_staff:
            if user.has_perm('product.view_product'): #app_name.verb_model_name
                return True
            if user.has_perm('product.change_product'): #
                return True
            if user.has_perm('product.delete_product'):#
                return True
            if user.has_perm('product.add_product'):#
                return True
        print(user.get_all_permissions())    
        return False

    