from rest_framework import serializers
from .models import Restaurant, Category, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'price', 'is_available', 'prep_to_min', 'category', 'restaurant']


class CategorySerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'restaurant', 'foods']


class RestaurantSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'address', 'latitude', 'longitude', 'is_open', 'category', 'foods',
                  'created_at']
