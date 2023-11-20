from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request,view):
        if request.method in permissions.SAFE_METHOD:
            return True
        return request.user.is_staff or request.user.is_admin