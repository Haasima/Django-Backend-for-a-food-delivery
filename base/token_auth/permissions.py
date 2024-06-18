from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """
    def has_permission(self, request, view):
        if request.method in ["GET", "PUT"]:
            return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user.is_staff
                    or obj == request.user)

        return (obj == request.user or request.user.is_staff or obj.user == request.user)