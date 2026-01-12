import json
from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from contact.modules.gateways.chatwoot.infrastructure.settings import get_base_url, get_api_token


def send_message(inbox_identifier: str, contact_identifier: str, conversation_id: str, content: str, echo_id: str) -> Dict[str, Any]:
    url = f"{get_base_url()}/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages"
    body = json.dumps({"content": content, "echo_id": echo_id}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }
    token = get_api_token()
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

