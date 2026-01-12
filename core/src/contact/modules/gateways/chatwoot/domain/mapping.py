from typing import Any, Dict
from contact.modules.gateways.chatwoot.domain.errors import InvalidPayload, UnsupportedEvent


def to_inbound_envelope(payload: Dict[str, Any]) -> Dict[str, Any]:
    event = payload.get("event")
    if event != "message_created":
        raise UnsupportedEvent("unsupported event")
    message = payload.get("message") or {}
    msg_id = str(message.get("id", "")) if message.get("id") is not None else ""
    content = message.get("content", "")
    message_type = message.get("message_type", "")
    conversation = payload.get("conversation") or {}
    conv_id = str(conversation.get("id", "")) if conversation.get("id") is not None else ""
    contact = conversation.get("contact") or {}
    contact_id = str(contact.get("id", "")) if contact.get("id") is not None else ""
    if not msg_id or not content or message_type != "incoming" or not conv_id or not contact_id:
        raise InvalidPayload("missing required fields")
    return {
        "provider": "chatwoot",
        "external_event_id": msg_id,
        "conversation_external_id": conv_id,
        "contact_external_id": contact_id,
        "content": content,
        "raw_payload": payload,
    }

