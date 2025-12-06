from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Cart, CartItem, OrderItem, Order
from .serializers import CartSerializer, OrderSerializer
from foods.models import Food
from rest_framework.generics import DestroyAPIView, GenericAPIView, ListAPIView, RetrieveAPIView


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        food_id = request.data.get('food')
        quantity = int(request.data.get('quantity', 1))

        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return Response({
                'error': 'Food not found'
            }, status=404)

        item, created = CartItem.objects.get_or_create(cart=cart, food=food)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity

        item.save()
        return Response({"message": "Added to cart"})


class RemoveFromCartView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer=request.user)
        food_id = request.data.get("food")

        try:
            item = CartItem.objects.get(cart=cart, food_id=food_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        item.delete()
        return Response({"message": "Removed from cart"})


class CreateOrderView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(customer=request.user)

        if cart.items.count() == 0:
            return Response({"error": "Cart is empty"}, status=400)

        restaurant = cart.items.first().food.restaurant

        order = Order.objects.create(
            customer=request.user,
            phone_number=request.user.phone_number,
            restaurant=restaurant
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=201)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
