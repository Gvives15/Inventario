import os
from django.conf import settings

def get_setting(name: str, default: str = "") -> str:
    val = getattr(settings, name, None)
    if val is None:
        return os.environ.get(name, default)
    return str(val)

def get_verify_token() -> str:
    return get_setting("WHATSAPP_VERIFY_TOKEN", "")

def get_app_secret() -> str:
    return get_setting("WHATSAPP_APP_SECRET", "")

def get_phone_number_id() -> str:
    return get_setting("WHATSAPP_PHONE_NUMBER_ID", "")

def get_access_token() -> str:
    return get_setting("WHATSAPP_ACCESS_TOKEN", "")

def get_catalog_id() -> str:
    return get_setting("WHATSAPP_CATALOG_ID", "")
