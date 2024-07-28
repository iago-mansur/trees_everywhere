from rest_framework.permissions import BasePermission

class IsAuthenticatedOr401(BasePermission):
    """
    Custom permission to return 401 Unauthorized for unauthenticated requests.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        self.message = 'Authentication credentials were not provided.'
        return False