from inventory.src.infrastructure.orm.stock_movement_repo import list_for_product

def execute(product_id: int, limit: int = 50):
    return list_for_product(product_id, limit)
