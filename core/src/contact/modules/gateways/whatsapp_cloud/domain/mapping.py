from typing import Any, Dict, List

def to_inbound_envelope(payload: Dict[str, Any]) -> Dict[str, Any]:
    entry = (payload or {}).get("entry", [])
    changes = entry[0].get("changes", []) if entry else []
    v = changes[0].get("value", {}) if changes else {}
    messages = v.get("messages", []) or []
    contacts = v.get("contacts", []) or []
    wa_id = contacts[0].get("wa_id") if contacts else None
    if not messages:
        return {}
    m = messages[0]
    mid = m.get("id")
    mtype = m.get("type") or ("text" if m.get("text") else None)
    content = None
    order_items = None
    interactive = None
    if mtype == "text":
        content = (m.get("text") or {}).get("body")
    elif mtype == "order":
        order_items = (m.get("order") or {}).get("product_items") or []
    elif mtype == "interactive":
        interactive = m.get("interactive") or {}
    return {
        "provider": "whatsapp_cloud",
        "external_event_id": mid,
        "contact_external_id": wa_id,
        "thread_key": wa_id,
        "message_type": mtype,
        "content": content,
        "interactive": interactive,
        "order_items": order_items,
        "raw_payload": payload,
    }

def to_inbound_envelopes(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    envelopes: List[Dict[str, Any]] = []
    entry = (payload or {}).get("entry", [])
    changes = entry[0].get("changes", []) if entry else []
    v = changes[0].get("value", {}) if changes else {}
    messages = v.get("messages", []) or []
    contacts = v.get("contacts", []) or []
    wa_id = contacts[0].get("wa_id") if contacts else None
    for m in messages:
        mid = m.get("id")
        mtype = m.get("type") or ("text" if m.get("text") else None)
        content = None
        order_items = None
        interactive = None
        if mtype == "text":
            content = (m.get("text") or {}).get("body")
        elif mtype == "order":
            order_items = (m.get("order") or {}).get("product_items") or []
        elif mtype == "interactive":
            interactive = m.get("interactive") or {}
        envelopes.append({
            "provider": "whatsapp_cloud",
            "external_event_id": mid,
            "contact_external_id": wa_id,
            "thread_key": wa_id,
            "message_type": mtype,
            "content": content,
            "interactive": interactive,
            "order_items": order_items,
            "raw_payload": payload,
        })
    return envelopes
