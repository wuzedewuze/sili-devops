from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser

class ObjectIsSelfuserOrSuperuser(permissions.BasePermission):
    """
    自定义角色如果是超级管理员或者是自己
    """
    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user or request.user.is_staff)

    # def has_permission(self, request, view):
    #     return request.user.is_staff

