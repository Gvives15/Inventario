from django.utils import timezone
from django.db.models import Sum, Count
from inventory.src.infrastructure.orm.models import StockMovement


def execute(limit: int = 10):
    now = timezone.now()
    last_7d = now - timezone.timedelta(days=7)

    top_exits = (
        StockMovement.objects.filter(created_at__gte=last_7d, movement_type=StockMovement.TYPE_EXIT)
        .values("product_id", "product__sku", "product__name")
        .annotate(units_sum=Sum("delta"))
        .order_by("units_sum")[:limit]
    )
    top_exits_out = [
        {"product_id": x["product_id"], "sku": x["product__sku"], "name": x["product__name"], "units": int(-(x["units_sum"] or 0))}
        for x in top_exits
    ]

    top_adjusts = (
        StockMovement.objects.filter(created_at__gte=last_7d, movement_type=StockMovement.TYPE_ADJUST)
        .values("product_id", "product__sku", "product__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:limit]
    )
    top_adjusts_out = [
        {"product_id": a["product_id"], "sku": a["product__sku"], "name": a["product__name"], "count": int(a["count"] or 0)}
        for a in top_adjusts
    ]

    return {
        "top_exits": top_exits_out,
        "top_adjusts": top_adjusts_out,
    }
