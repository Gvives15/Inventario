from django.db import transaction
import logging
from inventory.infrastructure.orm.product_repo import get_for_update
from inventory.infrastructure.orm.stock_movement_repo import create as create_movement
from inventory.domain.rules import validate_positive, require_reason
from inventory.domain.movement_types import MovementTypes
logger = logging.getLogger("inventory.movements")

def execute(product_id: int, quantity: int, reason: str, user=None, contact=None):
    validate_positive(quantity)
    require_reason(reason)
    with transaction.atomic():
        product = get_for_update(product_id)
        new_stock = product.stock_current + quantity
        create_movement(product, quantity, MovementTypes.ENTRY, reason, new_stock, user, contact)
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
                "contact_id": getattr(contact, "id", None),
            },
        )
        return product
