from typing import Any, Optional
from contact.modules.messaging.infrastructure.orm.message_event_repo import log_inbound


def execute(provider: str, external_event_id: str, conversation_external_id: str, contact_id: Optional[int], status: str, payload_json: Any):
    return log_inbound(provider, external_event_id, conversation_external_id, contact_id, status, payload_json)

