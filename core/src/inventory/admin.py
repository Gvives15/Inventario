from django.contrib import admin
from inventory.infrastructure.orm.models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "stock_current", "stock_minimum", "is_active", "updated_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("sku", "name")
    readonly_fields = ("created_at", "updated_at")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "product", "movement_type", "delta", "resulting_stock", "contact", "reason", "created_by")
    list_filter = ("movement_type", "contact__type", "created_at", "created_by")
    search_fields = ("product__sku", "product__name", "reason", "contact__name")
    readonly_fields = ("created_at", "resulting_stock")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
