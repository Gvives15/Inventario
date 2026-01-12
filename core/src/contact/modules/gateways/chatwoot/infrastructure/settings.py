import os
from django.conf import settings

def get_setting(name: str, default: str = "") -> str:
    # Try Django settings first, then os.environ
    val = getattr(settings, name, None)
    if val is None:
        return os.environ.get(name, default)
    return str(val)


def get_base_url() -> str:
    url = get_setting("CHATWOOT_BASE_URL")
    return url.rstrip("/") if url else "http://localhost"


def get_webhook_token() -> str:
    return get_setting("CHATWOOT_WEBHOOK_TOKEN", "")


def get_inbox_identifier() -> str:
    return get_setting("CHATWOOT_INBOX_ID", "")


def get_contact_identifier() -> str:
    return get_setting("CHATWOOT_CONTACT_ID", "")


def get_api_token() -> str:
    return get_setting("CHATWOOT_API_TOKEN", "")
