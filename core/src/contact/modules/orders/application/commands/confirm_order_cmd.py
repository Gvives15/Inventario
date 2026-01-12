from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.shared.domain.errors import ContactNotFound
from contact.modules.contacts.application.commands.refresh_contact_sku_stats_cmd import refresh_contact_sku_stats_cmd
from contact.models import OrderModel, OrderOpsEventModel

class InvalidOrderState(Exception):
    pass

def execute(whatsapp_id: str) -> int:
    with UnitOfWork() as uow:
        c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
        if not c:
            raise ContactNotFound("contact not found")
        st = uow.conversations.get_by_contact_id(c.id)
        if not st or not st.last_order_id:
            raise InvalidOrderState("no order to confirm")
        order = uow.orders.get(st.last_order_id)
        if order.status == "CONFIRMED":
            # Ensure ops_status is consistent even if already confirmed commercially
            if not order.ops_status:
                order.ops_status = OrderModel.OPS_CONFIRMED
                order.save(update_fields=["ops_status", "updated_at"])
            uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E4_CONFIRMED, order.id)
            refresh_contact_sku_stats_cmd(c.id)
            return order.id
        if order.status != "PROPOSED":
            raise InvalidOrderState("order not in PROPOSED")
        
        # Commercial Confirmation
        order.status = "CONFIRMED"
        
        # Ops Queue Entry
        order.ops_status = OrderModel.OPS_CONFIRMED
        
        order.save(update_fields=["status", "ops_status", "updated_at"])
        
        # Audit Log: Entry to Ops Queue
        OrderOpsEventModel.objects.create(
            order=order,
            from_status=OrderModel.OPS_CONFIRMED,
            to_status=OrderModel.OPS_CONFIRMED,
            note="Order confirmed via WhatsApp"
        )

        uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E4_CONFIRMED, order.id)
        refresh_contact_sku_stats_cmd(c.id)
        return order.id
