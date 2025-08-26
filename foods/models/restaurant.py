from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
