from rest_framework import permissions
from account.Utilities.permissions import IsSaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsSaffEditorPermission]