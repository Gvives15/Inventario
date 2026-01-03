from inventory.infrastructure.orm.models import ProductListModel, ProductListItemModel

def get_by_code(code: str) -> ProductListModel:
    return ProductListModel.objects.get(code=code)

def list_items(code: str):
    plist = get_by_code(code)
    return ProductListItemModel.objects.filter(product_list=plist).select_related("product").order_by("sort_order", "id")
