from inventory.infrastructure.orm.product_repo import list_products as repo_list

def execute(search: str | None = None, category: str | None = None):
    return repo_list(search=search, category=category)
