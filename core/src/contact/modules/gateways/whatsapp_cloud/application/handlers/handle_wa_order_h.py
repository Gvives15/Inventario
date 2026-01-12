from typing import List
from contact.modules.messaging.application.commands.log_inbound_event_cmd import execute as log_inbound
from contact.models import Contact, OrderModel, OrderItemModel, OrderOpsEventModel
from inventory.infrastructure.orm.models import Product
from contact.modules.gateways.whatsapp_cloud.application.handlers.send_wa_text_h import execute as send_text

def execute(env: dict) -> str:
    wa_id = env.get("thread_key")
    items = env.get("order_items") or []
    contact, _ = Contact.objects.get_or_create(whatsapp_id=wa_id, defaults={"name": wa_id, "business_type": "", "type": Contact.TYPE_CLIENT, "is_active": True})
    
    # Create with CONFIRMED initially, but ops_status depends on validation
    order = OrderModel.objects.create(contact=contact, status="CONFIRMED")
    
    unknown: List[str] = []
    for it in items:
        sku = it.get("product_retailer_id")
        qty = int(it.get("quantity") or 0)
        if not Product.objects.filter(sku=sku).exists():
            unknown.append(sku)
        OrderItemModel.objects.create(order=order, product_ref=sku or "", qty=qty)
    
    if unknown:
        order.status = "REQUIRES_REVIEW"
        order.ops_status = OrderModel.OPS_REQUIRES_REVIEW
        order.review_reason_code = OrderModel.REVIEW_SKU_UNKNOWN
        order.review_reason_note = f"Unknown SKUs: {unknown}"
        order.save(update_fields=["status", "ops_status", "review_reason_code", "review_reason_note", "updated_at"])
        
        OrderOpsEventModel.objects.create(
            order=order,
            to_status=OrderModel.OPS_REQUIRES_REVIEW,
            review_reason_code=OrderModel.REVIEW_SKU_UNKNOWN,
            note=f"Incoming WA Order with unknown SKUs: {unknown}"
        )
        
        log_inbound("whatsapp_cloud", f"wa:order:{env.get('external_event_id')}", wa_id or "", contact.id, "FAILED", {"unknown_skus": unknown})
        send_text(wa_id or "", "Recibimos tu pedido, pero hay productos que requieren verificación. Te confirmamos en breve.")
        return "REQUIRES_REVIEW"
    
    # Happy Path
    order.ops_status = OrderModel.OPS_CONFIRMED
    order.save(update_fields=["ops_status", "updated_at"])
    
    OrderOpsEventModel.objects.create(
        order=order,
        to_status=OrderModel.OPS_CONFIRMED,
        note="Incoming WA Order (Native)"
    )
    
    return "CONFIRMED"
