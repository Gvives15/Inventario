from inventory.infrastructure.orm.product_list_repo import get_by_code, list_items
from inventory.infrastructure.orm.models import ProductListModel
from inventory.domain.errors import ProductListNotFound, ProductListInactive, ProductListEmpty

def execute(code: str):
    try:
        plist = get_by_code(code)
    except ProductListModel.DoesNotExist:
        raise ProductListNotFound()
    if not plist.is_active:
        raise ProductListInactive()
    items_qs = list_items(code)
    if not items_qs.exists():
        raise ProductListEmpty()
    return {
        "code": plist.code,
        "name": plist.name,
        "items": [
            {
                "sku": item.product.sku,
                "name": item.product.name,
                "default_qty": int(item.default_qty),
            }
            for item in items_qs
        ],
    }
