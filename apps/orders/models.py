from django.db import models
from apps.foods.models import Food, Restaurant
from apps.users.models import CustomUser, phone_regex


class Cart(models.Model):
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.customer.phone_number}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'food')

    def __str__(self):
        return f"{self.quantity} x {self.food.title}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COOKED = 'COOKED', 'Cooked'
        ON_THE_WAY = 'ON_THE_WAY', 'On the way'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELED = 'CANCELED', 'Canceled'

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    phone_number = models.CharField(max_length=13, validators=[phone_regex])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price * self.quantity
