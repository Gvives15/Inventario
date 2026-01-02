from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.modules.conversations.application.parsers.parse_e1_block_p import parse as parse_e1
from contact.modules.conversations.application.commands.upsert_contact_min_data_cmd import execute as upsert_min
from contact.presenters.render_e1_prompt_p import render_e1_prompt, render_missing_fields
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_order
from contact.modules.orders.application.queries.get_order_summary_q import execute as order_summary
from contact.presenters.render_order_proposal_p import render as render_proposal


def execute(dto: dict) -> str:
    with UnitOfWork() as uow:
        created, _ = uow.inbound.create_if_new(dto)
        if not created:
            return "OK (duplicate ignored)"

        whatsapp_id = dto["whatsapp_id"]
        # ensure conversation state exists (even for placeholder)
        c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
        if c is None:
            c = uow.contacts.upsert_minimal(whatsapp_id, name="", zone="", business_type="")
        st = uow.conversations.get_by_contact_id(c.id)
        if st is None:
            uow.conversations.set_stage_and_last_order(c.id, ConversationStage.E1_MIN_DATA, None)
            st = uow.conversations.get_by_contact_id(c.id)

        # Check if already in E2 (Idempotency for chatty users)
        # Note: st.stage is a string (e.g. "E2_PROPOSAL"), not an Enum, when coming from Django model without choices conversion in repo
        current_stage = st.stage if isinstance(st.stage, str) else st.stage.value
        if current_stage == ConversationStage.E2_PROPOSAL.value and st.last_order_id:
            summary = order_summary(st.last_order_id)
            if summary and summary.get("status") == "PROPOSED":
                return render_proposal(summary)

        # v1: parse E1 and upsert minimal data
        found = parse_e1(dto.get("text", ""))
        if found:
            upsert_min(whatsapp_id, found.get("name"), found.get("zone"), found.get("business_type"))
            # recompute missing after update
            c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
            missing = []
            if not c.name:
                missing.append("Nombre")
            if not c.zone:
                missing.append("Zona")
            if not c.business_type:
                missing.append("Tipo")
            if missing:
                return render_missing_fields(missing)
            # E1 completo → siguiente paso (temporal)
            # idempotencia: si ya está en E2 y tiene propuesta PROPOSED, reusar (delegado en comandos/queries)
            order_id = create_order(whatsapp_id)
            summary = order_summary(order_id)
            return render_proposal(summary)

        # default prompt
        return render_e1_prompt()
