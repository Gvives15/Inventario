from inventory.application.queries.get_product_list_q import execute as get_list
from inventory.infrastructure.orm.models import Product
from inventory.domain.errors import ProductListNotFound, ProductListInactive, ProductListEmpty

def get_items():
    try:
        data = get_list("kiosk_base")
        items = [{"product_ref": f"SKU:{it['sku']}", "qty": int(it["default_qty"])} for it in data["items"]]
        if len(items) < 10:
            skus_in_list = {it["sku"] for it in data["items"]}
            extras = Product.objects.filter(is_active=True).exclude(sku__in=list(skus_in_list)).order_by("name", "sku")[: (15 - len(items))]
            items += [{"product_ref": f"SKU:{p.sku}", "qty": 2} for p in extras]
            while len(items) < 10 and items:
                items.append(items[-1])
        return items[:15]
    except (ProductListNotFound, ProductListInactive, ProductListEmpty):
        prods = list(Product.objects.filter(is_active=True).order_by("name", "sku")[:15])
        if prods:
            items = [{"product_ref": f"SKU:{p.sku}", "qty": 2} for p in prods]
            while len(items) < 10:
                items.append(items[-1])
            return items
        return [{"product_ref": "SKU:UNKNOWN", "qty": 2} for _ in range(10)]
