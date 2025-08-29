from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'restaurant')