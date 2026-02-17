from rest_framework import serializers
from .models import Cart, CartItem, OrderItem, Order


class CartItemSerializer(serializers.ModelSerializer):
    food_title = serializers.CharField(source='food.title', read_only=True)
    food_price = serializers.IntegerField(source='food.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'food', 'food_title', 'food_price', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    food_title = serializers.CharField(source='food.title', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'food_title', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'phone_number', 'restaurant', 'status', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order
