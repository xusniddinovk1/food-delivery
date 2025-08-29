from django.urls import path, include
from .views import RestaurantViewSet, CategoryViewSet, FoodViewSet, PublicRestaurantViewSet, PublicCategoryViewSet, \
    PublicFoodViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'restaurant', PublicRestaurantViewSet, basename='restaurants')
router.register(f'categories', PublicCategoryViewSet, basename='categories')
router.register(f'foods', PublicFoodViewSet, basename='foods')

router.register(r'my-restaurants', RestaurantViewSet, basename='my-restaurants')
router.register(r'my-categories', CategoryViewSet, basename='my-categories')
router.register(r'my-foods', FoodViewSet, basename='my-foods')

urlpatterns = [
    path('', include(router.urls))
]
