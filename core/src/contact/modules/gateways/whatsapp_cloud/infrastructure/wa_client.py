import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from contact.modules.gateways.whatsapp_cloud.infrastructure.settings import get_access_token, get_phone_number_id, get_setting

def get_send_url() -> str:
    base = get_setting("WA_GRAPH_BASE_URL", "https://graph.facebook.com").rstrip("/")
    ver = get_setting("WA_API_VERSION", "v17.0").strip("/")
    pn = get_phone_number_id()
    return f"{base}/{ver}/{pn}/messages"

def build_text_payload(to: str, text: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

def build_product_list_payload(to: str, catalog_id: str, product_retailer_ids: list[str]) -> dict:
    if not catalog_id:
        raise ValueError("catalog_id is required")
    if not product_retailer_ids:
        raise ValueError("product_retailer_ids cannot be empty")
    return {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "product_list",
            "body": {"text": "Te armé tu reposición sugerida. Ajustá en el carrito y enviá el pedido."},
            "action": {
                "catalog_id": catalog_id,
                "sections": [
                    {
                        "title": "Reposición base",
                        "product_items": [{"product_retailer_id": rid} for rid in product_retailer_ids],
                    }
                ],
            },
        },
    }

def _send(payload: dict) -> dict:
    url = get_send_url()
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    token = get_access_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return {"status": resp.status, "body": data}
    except HTTPError as e:
        return {"status": e.code, "error": str(e)}
    except URLError as e:
        return {"status": 0, "error": str(e)}

def send_text(to: str, text: str) -> dict:
    return _send(build_text_payload(to, text))

def send_product_list(to: str, catalog_id: str, product_retailer_ids: list[str]) -> dict:
    return _send(build_product_list_payload(to, catalog_id, product_retailer_ids))

