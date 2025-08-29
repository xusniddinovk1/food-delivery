from rest_framework.permissions import BasePermission

from foods.models import Restaurant


class IsRestaurantOwner(BasePermission):
    """
    Faqat role=RESTAURANT bo‘lgan va o‘z restorani mavjud userga ruxsat.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "role", None) != "RESTAURANT":
            return False
        # userga tegishli restoran bormi?
        return Restaurant.objects.filter(owner=user).exists()

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Restaurant obyektida
        if hasattr(obj, "owner_id"):
            return obj.owner_id == user.id
        # Category/Food obyektida
        if hasattr(obj, "restaurant") and hasattr(obj.restaurant, "owner_id"):
            return obj.restaurant.owner_id == user.id
        return False