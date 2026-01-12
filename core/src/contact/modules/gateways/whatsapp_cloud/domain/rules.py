import hmac
import hashlib
from typing import Dict
from contact.modules.gateways.whatsapp_cloud.infrastructure.settings import get_app_secret, get_verify_token

def validate_verify_token(received_token: str) -> bool:
    expected = get_verify_token()
    return bool(expected) and hmac.compare_digest(received_token or "", expected)

def validate_signature(headers: Dict[str, str], raw_body: bytes) -> bool:
    sig_header = None
    for k, v in headers.items():
        if k.lower() == "x-hub-signature-256":
            sig_header = v
            break
    if not sig_header or not sig_header.startswith("sha256="):
        return False
    provided = sig_header.split("=", 1)[1]
    secret = get_app_secret()
    if not secret:
        return False
    digest = hmac.new(secret.encode("utf-8"), raw_body or b"", hashlib.sha256).hexdigest()
    return hmac.compare_digest(provided, digest)

