from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.orders.application.templates.kiosk_template import get_kiosk_template
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.shared.domain.errors import ContactNotFound, MissingMinData


class MissingMinData(Exception):
    pass


def execute(whatsapp_id: str) -> int:
    with UnitOfWork() as uow:
        c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
        if not c:
            raise ContactNotFound("contact not found")
        if not c.name or not c.zone or not c.business_type:
            raise MissingMinData("contact missing minimal data")

        # idempotencia: si ya existe propuesta PROPOSED en E2, reusar
        st = uow.conversations.get_by_contact_id(c.id)
        if st and st.stage == ConversationStage.E2_PROPOSAL.value and st.last_order:
            last = uow.orders.get(st.last_order_id)
            if last.status == "PROPOSED":
                return last.id

        items = get_kiosk_template()
        order = uow.orders.create_proposed(c.id, items)
        uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E2_PROPOSAL, order.id)
        return order.id
