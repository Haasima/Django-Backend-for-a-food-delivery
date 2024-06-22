from rest_framework import permissions


class isOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.seller.user == request.user

class IsAdminOrCourier(permissions.BasePermission):
    """
    Custom permission to only allow courier of an object or admin users to view it.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user.is_staff
                    or (request.user.role == "COURIER" and obj.courier == request.user))
        return request.user.is_staff
        

class IsAdminOrCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customer of an object or admin users to view it.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user.is_staff
                    or (request.user.role == "CLIENT" and obj.customer == request.user))
        return request.user.is_staff