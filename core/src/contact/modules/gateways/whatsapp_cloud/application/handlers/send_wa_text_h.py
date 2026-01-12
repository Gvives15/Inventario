import uuid
from contact.modules.gateways.whatsapp_cloud.infrastructure.wa_client import send_text
from contact.modules.messaging.application.commands.log_outbound_event_cmd import execute as log_outbound

def execute(thread_key: str, content: str) -> str:
    echo_id = str(uuid.uuid4())
    log_outbound("whatsapp_cloud", echo_id, thread_key, None, "SENT", {"content": content})
    r = send_text(thread_key, content)
    if r.get("status", 0) == 200:
        return "OK"
    log_outbound("whatsapp_cloud", echo_id, thread_key, None, "FAILED", {"content": content, "error": r.get("error")})
    return "FAILED"

