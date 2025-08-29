from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from foods.models import Restaurant


@receiver(post_save, sender=CustomUser)
def create_restaurant_for_owner(sender, instance, created, **kwargs):
    if created and instance.role == CustomUser.Roles.RESTAURANT:
        if not instance.restaurant:
            restaurant = Restaurant.objects.create(
                name=f"{instance.username} Cafe",
                is_open=True
            )
            instance.restaurant = restaurant
            instance.save()
