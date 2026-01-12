import hmac
from contact.modules.gateways.chatwoot.infrastructure.settings import get_webhook_token


def validate_token(received: str) -> bool:
    expected = get_webhook_token()
    return bool(expected) and hmac.compare_digest(received or "", expected)

