from contact.models import OrderModel


def execute(order_id: int) -> dict:
    order = OrderModel.objects.select_related("contact").prefetch_related("items").get(id=order_id)
    items_data = [
        {"product_ref": i.product_ref, "qty": i.qty}
        for i in order.items.all()
    ]

    return {
        "order_id": order.id,
        "contact_name": order.contact.name,
        "contact_zone": order.contact.zone,
        "contact_business_type": order.contact.business_type,
        "status": order.status,
        "items": items_data,
    }
