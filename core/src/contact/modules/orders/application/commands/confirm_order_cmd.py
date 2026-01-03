from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.shared.domain.errors import ContactNotFound

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
            uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E4_CONFIRMED, order.id)
            return order.id
        if order.status != "PROPOSED":
            raise InvalidOrderState("order not in PROPOSED")
        order.status = "CONFIRMED"
        order.save(update_fields=["status", "updated_at"])
        uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E4_CONFIRMED, order.id)
        return order.id
