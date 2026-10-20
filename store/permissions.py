from rest_framework.permissions import BasePermission, SAFE_METHODS
def is_admin(user):
    return bool(user and user.is_authenticated and (user.is_staff or user.role=="admin"))
class IsAdminOrReadOnly(BasePermission):
     def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return (
            user.is_authenticated
            and (
                user.is_staff
                or user.is_superuser
                or getattr(user, "role", None) == "admin"
            )
        )
class IsAdminRole(BasePermission):
      def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and (
                user.is_staff
                or user.is_superuser
                or getattr(user, "role", None) == "admin"
            )
        )
