from rest_framework import viewsets
from .serializers import RestaurantSerializer, CategorySerializer, FoodSerializer
from .models import Restaurant, Category, Food
from rest_framework.permissions import AllowAny, IsAuthenticated


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.filter(is_open=True)
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]
        return [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Food.objects.filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)
