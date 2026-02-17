from django.urls import include
from .views import RestaurantViewSet, CategoryViewSet, FoodViewSet, PublicRestaurantViewSet, PublicCategoryViewSet, \
    PublicFoodViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.orders.views import (
    CartView, RemoveFromCartView,
    CreateOrderView, OrderListView, OrderDetailView
)

router = DefaultRouter()
router.register(f'restaurant', PublicRestaurantViewSet, basename='restaurants')
router.register(f'categories', PublicCategoryViewSet, basename='categories')
router.register(f'foods', PublicFoodViewSet, basename='foods')

router.register(r'my-restaurants', RestaurantViewSet, basename='my-restaurants')
router.register(r'my-categories', CategoryViewSet, basename='my-categories')
router.register(r'my-foods', FoodViewSet, basename='my-foods')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path("cart/", CartView.as_view()),
    path("cart/remove/", RemoveFromCartView.as_view()),
    path("order/create/", CreateOrderView.as_view()),
    path("orders/", OrderListView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
]
