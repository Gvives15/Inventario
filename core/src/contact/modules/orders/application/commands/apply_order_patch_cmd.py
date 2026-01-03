from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from inventory.infrastructure.orm.models import Product
from contact.shared.domain.errors import ContactNotFound

class InvalidAction(Exception):
    pass

class InvalidQuantity(Exception):
    pass

class ProductNotFound(Exception):
    pass

def execute(whatsapp_id: str, action: dict) -> int:
    with UnitOfWork() as uow:
        c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
        if not c:
            raise ContactNotFound("contact not found")
        st = uow.conversations.get_by_contact_id(c.id)
        if not st or not st.last_order_id:
            raise InvalidAction("no order to patch")
        order = uow.orders.get(st.last_order_id)
        if order.status != "PROPOSED":
            raise InvalidAction("order not editable")
        act = (action or {}).get("action")
        if act not in ("ADD", "REMOVE", "SET_QTY"):
            raise InvalidAction("unsupported action")
        sku = (action or {}).get("sku")
        if act in ("ADD", "SET_QTY"):
            qty = int((action or {}).get("qty", 0))
            if qty <= 0:
                raise InvalidQuantity("qty must be > 0")
        if sku:
            try:
                Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                raise ProductNotFound("sku not found")
        # apply changes
        items = {it.product_ref: it for it in order.items.all()}
        ref = f"SKU:{sku}" if sku else None
        if act == "ADD":
            if ref in items:
                item = items[ref]
                item.qty = int(item.qty) + qty
                item.save(update_fields=["qty"])
            else:
                from contact.models import OrderItemModel
                OrderItemModel.objects.create(order=order, product_ref=ref, qty=qty)
        elif act == "REMOVE":
            if ref in items:
                items[ref].delete()
        elif act == "SET_QTY":
            if ref in items:
                item = items[ref]
                item.qty = qty
                item.save(update_fields=["qty"])
            else:
                from contact.models import OrderItemModel
                OrderItemModel.objects.create(order=order, product_ref=ref, qty=qty)
        uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E3_ADJUSTMENTS, order.id)
        return order.id
