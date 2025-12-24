from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=128, blank=True)
    stock_current = models.IntegerField(default=0)
    stock_minimum = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class StockMovement(models.Model):
    TYPE_ENTRY = "entry"
    TYPE_EXIT = "exit"
    TYPE_ADJUST = "adjust"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    delta = models.IntegerField()
    movement_type = models.CharField(max_length=16)
    reason = models.CharField(max_length=255, blank=True)
    resulting_stock = models.IntegerField()
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
