import uuid
from contact.modules.gateways.whatsapp_cloud.infrastructure.wa_client import send_product_list
from contact.modules.gateways.whatsapp_cloud.infrastructure.settings import get_catalog_id
from contact.modules.messaging.application.commands.log_outbound_event_cmd import execute as log_outbound

def execute(thread_key: str, sku_list: list[str]) -> str:
    echo_id = str(uuid.uuid4())
    catalog_id = get_catalog_id()
    log_outbound("whatsapp_cloud", echo_id, thread_key, None, "SENT", {"skus": sku_list})
    r = send_product_list(thread_key, catalog_id, sku_list)
    if r.get("status", 0) == 200:
        return "OK"
    log_outbound("whatsapp_cloud", echo_id, thread_key, None, "FAILED", {"skus": sku_list, "error": r.get("error")})
    return "FAILED"

