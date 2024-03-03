from rest_framework import permissions

from account.permissions import IsSaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsSaffEditorPermission]