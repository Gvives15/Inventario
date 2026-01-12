import uuid
from contact.modules.gateways.chatwoot.infrastructure import chatwoot_client
from contact.modules.gateways.chatwoot.infrastructure.settings import get_inbox_identifier, get_contact_identifier
from contact.modules.messaging.application.commands.log_outbound_event_cmd import execute as log_outbound


def execute(conversation_id: str, content: str) -> str:
    echo_id = str(uuid.uuid4())
    inbox_id = get_inbox_identifier()
    contact_id = get_contact_identifier()
    log_outbound("chatwoot", echo_id, conversation_id, None, "SENT", {"content": content})
    r = chatwoot_client.send_message(inbox_id, contact_id, conversation_id, content, echo_id)
    if r.get("status", 0) == 200:
        return "OK"
    log_outbound("chatwoot", echo_id, conversation_id, None, "FAILED", {"content": content, "error": r.get("error")})
    return "FAILED"
