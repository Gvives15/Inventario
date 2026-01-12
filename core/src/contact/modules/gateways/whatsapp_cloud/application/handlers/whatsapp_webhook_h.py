from typing import Any, Dict, Tuple
from contact.modules.gateways.whatsapp_cloud.domain.rules import validate_verify_token, validate_signature
from contact.modules.gateways.whatsapp_cloud.domain.mapping import to_inbound_envelopes
from contact.modules.messaging.application.commands.log_inbound_event_cmd import execute as log_inbound
from contact.modules.messaging.application.queries.was_event_processed_q import execute as was_event_processed
from contact.modules.gateways.whatsapp_cloud.application.handlers.handle_wa_order_h import execute as handle_order

def execute_verify(params: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    mode = params.get("hub.mode", "") or params.get("hub.mode".upper(), "")
    token = params.get("hub.verify_token", "") or params.get("hub.verify_token".upper(), "")
    challenge = params.get("hub.challenge", "") or params.get("hub.challenge".upper(), "")
    if mode != "subscribe":
        return {"error": "invalid_mode"}, 401
    if not validate_verify_token(token):
        return {"error": "unauthorized"}, 401
    return {"hub.challenge": challenge}, 200

def execute_inbound(headers: Dict[str, str], raw_body: bytes, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    if not validate_signature(headers, raw_body):
        return {"error": "unauthorized"}, 401
    envs = to_inbound_envelopes(payload)
    for env in envs:
        if not env or not env.get("external_event_id") or not env.get("contact_external_id"):
            # Campos críticos faltantes
            log_inbound("whatsapp_cloud", "wa:in:unknown", "", None, "FAILED", {"reason": "missing_fields", "payload": payload})
            return {"error": "bad_request"}, 400
        provider = env["provider"]
        mid = env["external_event_id"]
        dedupe_key = f"wa:in:{mid}"
        thread_key = env.get("thread_key") or ""
        # Log RECEIVED siempre; si ya estaba PROCESSED, se registrará duplicado
        log_inbound(provider, dedupe_key, thread_key, None, "RECEIVED", env)
        if was_event_processed(provider, dedupe_key):
            # duplicado: no reprocesar ni cambiar estado final
            continue
        if env.get("message_type") == "order":
            handle_order(env)
            log_inbound(provider, dedupe_key, thread_key, None, "PROCESSED", env)
        else:
            log_inbound(provider, dedupe_key, thread_key, None, "PROCESSED", env)
    return {"ok": True}, 200
