from django.urls import path, include
from .views import RestaurantViewSet, CategoryViewSet, FoodViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'restaurant', RestaurantViewSet, basename='restaurants')
router.register(f'categories', CategoryViewSet, basename='categories')
router.register(f'foods', FoodViewSet, basename='foods')

urlpatterns = [
    path('', include(router.urls))
]
