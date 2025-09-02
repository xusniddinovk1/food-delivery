from django.db import transaction
from .models import Order, OrderItem, Cart, CartItem


@transaction.atomic
def create_order_from_cart(customer, phone_number):
    # 1. Foydalanuvchi cartini topamiz
    cart = Cart.objects.get(customer=customer)
    items = cart.items.select_related("food")

    if not items.exists():
        raise ValueError("Cart bo‘sh. Buyurtma berib bo‘lmaydi.")

    # 2. Restaurantni aniqlash (hamma ovqat bitta restoran bo‘lishi shart)
    restaurants = {item.food.restaurant for item in items}
    if len(restaurants) > 1:
        raise ValueError("Cartda bir nechta restorandan ovqat bor.")

    restaurant = restaurants.pop()

    # 3. Order yaratamiz
    order = Order.objects.create(
        customer=customer,
        phone_number=phone_number,
        restaurant=restaurant,
    )

    # 4. CartItem → OrderItem
    order_items = []
    for item in items:
        order_items.append(OrderItem(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price  # Food narxidan olamiz
        ))
    OrderItem.objects.bulk_create(order_items)

    # 5. Cartni tozalash
    items.delete()

    return order
