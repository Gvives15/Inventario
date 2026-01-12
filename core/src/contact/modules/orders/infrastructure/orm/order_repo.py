from typing import Sequence, List
from contact.models import OrderModel, OrderItemModel


def create_proposed(contact_id: int, items: Sequence[dict]) -> OrderModel:
    order = OrderModel.objects.create(contact_id=contact_id, status="PROPOSED")
    bulk = []
    for it in items:
        ref = it.get("product_ref")
        qty = int(it.get("qty", 0))
        if not ref or qty <= 0:
            raise ValueError("invalid item")
        bulk.append(OrderItemModel(order=order, product_ref=str(ref), qty=qty))
    OrderItemModel.objects.bulk_create(bulk)
    return order


def get(order_id: int) -> OrderModel:
    return OrderModel.objects.prefetch_related("items").get(id=order_id)

def get_confirmed_by_contact(contact_id: int) -> List[OrderModel]:
    return list(OrderModel.objects.filter(contact_id=contact_id, status="CONFIRMED").order_by("-created_at"))
