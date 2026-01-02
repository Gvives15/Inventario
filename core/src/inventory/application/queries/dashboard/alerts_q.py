from django.db.models import F
from inventory.infrastructure.orm.models import Product, StockMovement
from inventory.domain.movement_types import MovementTypes


def execute(limit_low_stock: int = 10, limit_adjustments: int = 10):
    low_stock_qs = Product.objects.filter(
        is_active=True,
        stock_current__lte=F("stock_minimum"),
    ).order_by("stock_current", "sku")[:limit_low_stock]

    low_stock = [
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "stock_current": p.stock_current,
            "stock_minimum": p.stock_minimum,
        }
        for p in low_stock_qs
    ]

    recent_adjustments_qs = (
        StockMovement.objects.filter(movement_type__in=[MovementTypes.ADJUST_COUNT, MovementTypes.ADJUST_DELTA])
        .select_related("product", "created_by")
        .order_by("-created_at", "-id")[:limit_adjustments]
    )

    recent_adjustments = [
        {
            "id": m.id,
            "product_id": m.product_id,
            "sku": m.product.sku,
            "name": m.product.name,
            "delta": m.delta,
            "reason": m.reason,
            "resulting_stock": m.resulting_stock,
            "created_by": (m.created_by.username if m.created_by else ""),
            "created_at": m.created_at,
        }
        for m in recent_adjustments_qs
    ]

    return {
        "low_stock": low_stock,
        "recent_adjustments": recent_adjustments,
    }
