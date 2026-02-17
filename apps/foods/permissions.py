from rest_framework.permissions import BasePermission
from apps.foods.models import Restaurant


class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "role", None) != "RESTAURANT":
            return False

        if request.method == "POST":
            return not Restaurant.objects.filter(owner=user).exists()

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, "owner_id"):
            return obj.owner_id == user.id
        if hasattr(obj, "restaurant") and hasattr(obj.restaurant, "owner_id"):
            return obj.restaurant.owner_id == user.id
        return False
