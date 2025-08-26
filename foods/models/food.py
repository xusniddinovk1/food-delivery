from django.db import models
from .restaurant import Restaurant, Category


class Food(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_in_stock(self):
        return self.stock > 0

    def increase_stock(self, amount):
        self.stock += amount
        self.save()
        return self.stock

    def reduce_stock(self, quantity):
        if self.stock < quantity:
            raise False

        self.stock -= quantity
        self.save()
        return self.stock

    class Meta:
        ordering = ['title']
