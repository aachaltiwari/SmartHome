from rest_framework import permissions


class AdminOnlyRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = []
        self.perms_map['HEAD'] = []
        self.perms_map['POST'] = ['%(app_label)s.add_%(model_name)s']
        self.perms_map['PUT'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['PATCH'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['DELETE'] = ['%(app_label)s.delete_%(model_name)s']

