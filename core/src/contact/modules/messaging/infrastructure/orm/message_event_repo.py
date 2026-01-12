from typing import Any, Optional
from django.db import transaction
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel


@transaction.atomic
def log_inbound(provider: str, external_event_id: str, conversation_external_id: str, contact_id: Optional[int], status: str, payload_json: Any) -> MessageEventLogModel:
    existing = MessageEventLogModel.objects.filter(provider=provider, external_event_id=external_event_id).first()
    if existing and existing.status == "PROCESSED":
        dup = MessageEventLogModel.objects.create(
            provider=provider,
            direction="IN",
            external_event_id=f"dup:{external_event_id}",
            conversation_external_id=conversation_external_id,
            contact_id=contact_id,
            status="SKIPPED_DUPLICATE" if status == "RECEIVED" else status,
            payload_json=payload_json,
        )
        return dup
    defaults = {
        "direction": "IN",
        "conversation_external_id": conversation_external_id,
        "contact_id": contact_id,
        "status": status,
        "payload_json": payload_json,
    }
    obj, _ = MessageEventLogModel.objects.update_or_create(provider=provider, external_event_id=external_event_id, defaults=defaults)
    return obj


@transaction.atomic
def log_outbound(provider: str, echo_id: str, conversation_external_id: str, contact_id: Optional[int], status: str, payload_json: Any, external_event_id: Optional[str] = None) -> MessageEventLogModel:
    defaults = {
        "direction": "OUT",
        "conversation_external_id": conversation_external_id,
        "contact_id": contact_id,
        "status": status,
        "payload_json": payload_json,
        "external_event_id": external_event_id,
    }
    obj, _ = MessageEventLogModel.objects.update_or_create(provider=provider, echo_id=echo_id, defaults=defaults)
    return obj


def was_event_processed(provider: str, external_event_id: str) -> bool:
    return MessageEventLogModel.objects.filter(provider=provider, external_event_id=external_event_id, status="PROCESSED").exists()

def was_echo_logged(provider: str, echo_id: str) -> bool:
    return MessageEventLogModel.objects.filter(provider=provider, echo_id=echo_id).exists()
