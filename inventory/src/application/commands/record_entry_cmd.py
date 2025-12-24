from django.db import transaction
import logging
from inventory.src.infrastructure.orm.product_repo import get_for_update
from inventory.src.infrastructure.orm.stock_movement_repo import create as create_movement
from inventory.src.domain.rules import validate_positive
from inventory.src.domain.movement_types import MovementTypes
logger = logging.getLogger("inventory.movements")

def execute(product_id: int, quantity: int, reason: str, user=None):
    validate_positive(quantity)
    with transaction.atomic():
        product = get_for_update(product_id)
        new_stock = product.stock_current + quantity
        create_movement(product, quantity, MovementTypes.ENTRY, reason, new_stock, user)
        product.stock_current = new_stock
        product.save(update_fields=["stock_current", "updated_at"])
        logger.info(
            "entry",
            extra={
                "product_id": product.id,
                "sku": product.sku,
                "type": MovementTypes.ENTRY,
                "delta": quantity,
                "stock": new_stock,
                "reason": reason,
                "user_id": getattr(user, "id", None),
            },
        )
        return product
