from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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

from contact.models import Contact

class StockMovement(models.Model):
    TYPE_ENTRY = "entry"
    TYPE_EXIT = "exit"
    TYPE_ADJUST_COUNT = "adjust_count"
    TYPE_ADJUST_DELTA = "adjust_delta"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    delta = models.IntegerField()
    movement_type = models.CharField(
        max_length=16,
        choices=[
            (TYPE_ENTRY, TYPE_ENTRY),
            (TYPE_EXIT, TYPE_EXIT),
            (TYPE_ADJUST_COUNT, TYPE_ADJUST_COUNT),
            (TYPE_ADJUST_DELTA, TYPE_ADJUST_DELTA),
        ],
    )
    reason = models.CharField(max_length=255, blank=True)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="movements")
    resulting_stock = models.IntegerField()
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(movement_type__in=[
                    "entry",
                    "exit",
                    "adjust_count",
                    "adjust_delta",
                ]),
                name="movement_type_valid_choices",
            ),
        ]

class ProductListModel(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ["code"]

class ProductListItemModel(models.Model):
    product_list = models.ForeignKey(ProductListModel, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="list_items")
    default_qty = models.IntegerField()
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["product_list", "product"], name="uniq_product_in_list"),
            models.CheckConstraint(check=models.Q(default_qty__gt=0), name="check_default_qty_gt_0"),
        ]
