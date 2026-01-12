from typing import Any, Dict
from contact.modules.gateways.chatwoot.domain.rules import validate_token
from contact.modules.gateways.chatwoot.domain.mapping import to_inbound_envelope
from contact.modules.messaging.application.queries.was_event_processed_q import execute as was_event_processed
from contact.modules.messaging.application.commands.log_inbound_event_cmd import execute as log_inbound
from contact.modules.conversations.application.handlers.handle_whatsapp_inbound_h import execute as handle_text
from contact.modules.contacts.application.commands.resolve_chatwoot_identity_cmd import execute as resolve_identity


def execute(headers: Dict[str, str], payload: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
    token = headers.get("X-O11CE-Webhook-Token", "")
    if not validate_token(token):
        return {"error": "unauthorized"}, 401
    env = to_inbound_envelope(payload)
    if was_event_processed(env["provider"], env["external_event_id"]):
        log_inbound(env["provider"], env["external_event_id"], env["conversation_external_id"], None, "RECEIVED", env)
        return {"ok": True}, 200
    log_inbound(env["provider"], env["external_event_id"], env["conversation_external_id"], None, "RECEIVED", env)
    contact_id = resolve_identity(env["contact_external_id"], env["conversation_external_id"])
    dto = {
        "provider": env["provider"],
        "provider_message_id": env["external_event_id"],
        "whatsapp_id": f"chatwoot:{env['contact_external_id']}",
        "text": env["content"],
        "raw_payload": env["raw_payload"],
    }
    reply = handle_text(dto)
    log_inbound(env["provider"], env["external_event_id"], env["conversation_external_id"], None, "PROCESSED", env)
    return {"reply": reply}, 200
