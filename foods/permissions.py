from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "RESTAURANT"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
