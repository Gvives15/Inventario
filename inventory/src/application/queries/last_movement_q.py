from inventory.src.infrastructure.orm.stock_movement_repo import list_for_product

def execute(product_id: int):
    movements = list_for_product(product_id, limit=1)
    if movements:
        return movements[0]
    return None
