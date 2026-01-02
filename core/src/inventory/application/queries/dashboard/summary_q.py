from django.utils import timezone
from django.db.models import F
from inventory.infrastructure.orm.models import Product, StockMovement


def execute():
    now = timezone.now()
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_7d = now - timezone.timedelta(days=7)

    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()

    low_stock_count = Product.objects.filter(
        is_active=True,
        stock_current__lte=F("stock_minimum"),
    ).count()

    movements_today = StockMovement.objects.filter(created_at__gte=start_today).count()

    adjustments_7d = StockMovement.objects.filter(
        created_at__gte=last_7d,
        movement_type=StockMovement.TYPE_ADJUST,
    ).count()

    return {
        "total_products": total_products,
        "active_products": active_products,
        "low_stock_count": low_stock_count,
        "movements_today": movements_today,
        "adjustments_7d": adjustments_7d,
    }
