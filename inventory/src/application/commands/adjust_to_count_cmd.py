from django.db import transaction
import logging
from inventory.src.infrastructure.orm.product_repo import get_for_update
from inventory.src.infrastructure.orm.stock_movement_repo import create as create_movement
from inventory.src.domain.rules import ensure_non_negative, require_reason
from inventory.src.domain.movement_types import MovementTypes
logger = logging.getLogger("inventory.movements")

def execute(product_id: int, counted_stock: int, reason: str, user=None):
    require_reason(reason)
    ensure_non_negative(counted_stock)
    with transaction.atomic():
        product = get_for_update(product_id)
        delta = counted_stock - product.stock_current
        create_movement(product, delta, MovementTypes.ADJUST_COUNT, reason, counted_stock, user)
        product.stock_current = counted_stock
        product.save(update_fields=["stock_current", "updated_at"])
        logger.info(
            "adjust_to_count",
            extra={
                "product_id": product.id,
                "sku": product.sku,
                "type": MovementTypes.ADJUST_COUNT,
                "delta": delta,
                "stock": counted_stock,
                "reason": reason,
                "user_id": getattr(user, "id", None),
            },
        )
        return product
