from typing import List, Dict, Any
import hashlib
from datetime import date
import json

from contact.modules.gateways.whatsapp_cloud.infrastructure.wa_client import (
    send_text, 
    send_product_list,
    build_text_payload,
    build_product_list_payload
)
from contact.modules.messaging.infrastructure.orm.message_event_repo import log_outbound, was_echo_logged

def _get_day_bucket() -> str:
    return date.today().isoformat()

def _calculate_dedupe_key(wa_id: str, payload: Dict[str, Any]) -> str:
    # payload to string canonical
    p_str = json.dumps(payload, sort_keys=True)
    h = hashlib.sha1(p_str.encode("utf-8")).hexdigest()
    bucket = _get_day_bucket()
    return f"wa:out:{wa_id}:{h}:{bucket}"

def send_safe_text(to: str, text: str, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload = build_text_payload(to, text)
    if meta:
        payload["meta"] = meta
    dedupe_key = _calculate_dedupe_key(to, payload)
    
    if was_echo_logged("whatsapp_cloud", dedupe_key):
        return {"status": "skipped", "reason": "duplicate", "dedupe_key": dedupe_key}
        
    resp = send_text(to, text)
    
    status = "SENT" if resp.get("status") == 200 else "FAILED"
    log_outbound(
        provider="whatsapp_cloud",
        echo_id=dedupe_key,
        conversation_external_id=to,
        contact_id=None, 
        status=status,
        payload_json=payload,
        external_event_id=dedupe_key 
    )
    return resp

def send_safe_product_list(to: str, catalog_id: str, product_retailer_ids: List[str], proposal_source: str | None = None, contact_id: int | None = None, list_code: str | None = None) -> Dict[str, Any]:
    payload = build_product_list_payload(to, catalog_id, product_retailer_ids)
    if proposal_source:
        payload["proposal_source"] = proposal_source
    if list_code:
        payload["list_code"] = list_code
    if contact_id is not None:
        payload["contact_id"] = contact_id
    payload["skus_count"] = len(product_retailer_ids)
    dedupe_key = _calculate_dedupe_key(to, payload)
    
    if was_echo_logged("whatsapp_cloud", dedupe_key):
        return {"status": "skipped", "reason": "duplicate", "dedupe_key": dedupe_key}
        
    resp = send_product_list(to, catalog_id, product_retailer_ids)
    
    status = "SENT" if resp.get("status") == 200 else "FAILED"
    log_outbound(
        provider="whatsapp_cloud",
        echo_id=dedupe_key,
        conversation_external_id=to,
        contact_id=contact_id,
        status=status,
        payload_json=payload,
        external_event_id=dedupe_key
    )
    return resp
