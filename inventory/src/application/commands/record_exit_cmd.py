from django.db import transaction
from inventory.src.infrastructure.orm.product_repo import get_for_update
from inventory.src.infrastructure.orm.stock_movement_repo import create as create_movement
from inventory.src.domain.rules import validate_positive, ensure_non_negative
from inventory.src.domain.movement_types import MovementTypes

def execute(product_id: int, quantity: int, reason: str, user=None):
    validate_positive(quantity)
    with transaction.atomic():
        product = get_for_update(product_id)
        new_stock = product.stock_current - quantity
        ensure_non_negative(new_stock)
        create_movement(product, -quantity, MovementTypes.EXIT, reason, new_stock, user)
        product.stock_current = new_stock
        product.save(update_fields=["stock_current", "updated_at"])
        return product
