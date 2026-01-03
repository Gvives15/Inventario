from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.modules.conversations.application.parsers.parse_e1_block_p import parse as parse_e1
from contact.modules.conversations.application.commands.upsert_contact_min_data_cmd import execute as upsert_min
from contact.presenters.render_e1_prompt_p import render_e1_prompt, render_missing_fields
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_order
from contact.modules.orders.application.queries.get_order_summary_q import execute as order_summary
from contact.presenters.render_order_proposal_p import render as render_proposal
from contact.modules.conversations.application.parsers.parse_e2_actions_p import parse as parse_e2
from contact.modules.orders.application.commands.apply_order_patch_cmd import execute as apply_patch
from contact.modules.orders.application.commands.confirm_order_cmd import execute as confirm_order
from contact.presenters.render_order_updated_p import render as render_updated
from contact.presenters.render_order_confirmed_p import render as render_confirmed


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

        # Stage-based routing
        current_stage = st.stage if isinstance(st.stage, str) else st.stage.value
        if current_stage == ConversationStage.E2_PROPOSAL.value and st.last_order_id:
            action = parse_e2(dto.get("text", ""))
            if action["action"] == "SHOW":
                summary = order_summary(st.last_order_id)
                return render_proposal(summary)
            if action["action"] == "CONFIRM":
                oid = confirm_order(whatsapp_id)
                summary = order_summary(oid)
                return render_confirmed(summary)
            if action["action"] in ("ADD", "REMOVE", "SET_QTY"):
                st.stage = ConversationStage.E3_ADJUSTMENTS.value
                st.save(update_fields=["stage", "updated_at"])
                oid = apply_patch(whatsapp_id, action)
                summary = order_summary(oid)
                return render_updated(summary)
            if action["action"] == "UNKNOWN":
                summary = order_summary(st.last_order_id)
                prop = render_proposal(summary) if summary else ""
                return prop + "\n\nComandos válidos:\nOK: confirmar\nVER: ver propuesta\n+ SKU qty: agregar/sumar\n- SKU: quitar\n= SKU qty: fijar cantidad"
            summary = order_summary(st.last_order_id)
            if summary and summary.get("status") == "PROPOSED":
                return render_proposal(summary)
            return render_e1_prompt()

        if current_stage == ConversationStage.E3_ADJUSTMENTS.value and st.last_order_id:
            action = parse_e2(dto.get("text", ""))
            if action["action"] in ("ADD", "REMOVE", "SET_QTY"):
                oid = apply_patch(whatsapp_id, action)
                summary = order_summary(oid)
                return render_updated(summary)
            if action["action"] == "CONFIRM":
                oid = confirm_order(whatsapp_id)
                summary = order_summary(oid)
                return render_confirmed(summary)
            if action["action"] == "SHOW":
                summary = order_summary(st.last_order_id)
                return render_updated(summary)
            summary = order_summary(st.last_order_id)
            return render_updated(summary) + "\n\nAyuda: +/-/= para editar, OK para confirmar."

        if current_stage == ConversationStage.E4_CONFIRMED.value and st.last_order_id:
            summary = order_summary(st.last_order_id)
            return render_confirmed(summary)

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
