from inventory.src.infrastructure.orm.product_repo import list_low_stock as repo_list_low

def execute():
    return repo_list_low()
