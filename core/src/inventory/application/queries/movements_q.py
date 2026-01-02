from datetime import datetime, timedelta
from inventory.infrastructure.orm.models import StockMovement, Product
from inventory.domain.rules import normalize_sku

def list_movements(days: int | None = None, sku: str | None = None, movement_type: str | None = None, limit: int = 200):
    qs = StockMovement.objects.select_related("product", "created_by")
    if days is not None:
        since = datetime.utcnow() - timedelta(days=days)
        qs = qs.filter(created_at__gte=since)
    if sku:
        s = normalize_sku(sku)
        qs = qs.filter(product__sku=s)
    if movement_type:
        qs = qs.filter(movement_type=movement_type)
    return qs.order_by("-created_at", "-id")[:limit]
