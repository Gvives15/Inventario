from typing import Any, Optional
from contact.modules.messaging.infrastructure.orm.message_event_repo import log_outbound


def execute(provider: str, echo_id: str, conversation_external_id: str, contact_id: Optional[int], status: str, payload_json: Any, external_event_id: Optional[str] = None):
    return log_outbound(provider, echo_id, conversation_external_id, contact_id, status, payload_json, external_event_id)

