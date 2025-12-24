from inventory.src.infrastructure.orm.models import StockMovement, Product
from inventory.src.domain.movement_types import MovementTypes

def create(product: Product, delta: int, movement_type: str, reason: str, resulting_stock: int, user=None) -> StockMovement:
    allowed = {MovementTypes.ENTRY, MovementTypes.EXIT, MovementTypes.ADJUST_COUNT, MovementTypes.ADJUST_DELTA}
    if movement_type not in allowed:
        raise ValueError("invalid movement_type")
    return StockMovement.objects.create(
        product=product,
        delta=delta,
        movement_type=movement_type,
        reason=reason or "",
        resulting_stock=resulting_stock,
        created_by=user,
    )

def list_for_product(product_id: int, limit: int = 50):
    return StockMovement.objects.filter(product_id=product_id).order_by("-created_at", "-id")[:limit]
