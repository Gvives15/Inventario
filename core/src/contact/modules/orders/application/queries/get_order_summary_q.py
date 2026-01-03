from contact.models import OrderModel
from inventory.application.queries.get_products_by_skus_q import execute as get_names


def execute(order_id: int) -> dict:
    order = OrderModel.objects.select_related("contact").prefetch_related("items").get(id=order_id)
    items = list(order.items.all())
    skus = []
    for i in items:
        ref = str(i.product_ref or "")
        if ref.startswith("SKU:"):
            skus.append(ref.split("SKU:", 1)[1])
    name_map = get_names(skus)
    items_data = []
    for i in items:
        ref = str(i.product_ref or "")
        name = ""
        if ref.startswith("SKU:"):
            sku = ref.split("SKU:", 1)[1]
            name = name_map.get(sku, "sku desconocido")
        items_data.append({"product_ref": ref, "qty": i.qty, "product_name": name})

    return {
        "order_id": order.id,
        "contact_name": order.contact.name,
        "contact_zone": order.contact.zone,
        "contact_business_type": order.contact.business_type,
        "status": order.status,
        "items": items_data,
    }
