from typing import Any
from contact.modules.contacts.domain.keys import is_allowed_fact_key
from contact.modules.contacts.domain.rules import validate_fact_value
from contact.modules.contacts.infrastructure.orm.contact_history_repo import upsert_fact


def upsert_contact_fact_cmd(
    contact_id: int,
    key: str,
    value_json: Any,
    source: str,
    confidence: float = 1.0,
):
    if not is_allowed_fact_key(key):
        raise ValueError("fact key not allowed")
    validate_fact_value(key, value_json)
    return upsert_fact(contact_id, key, value_json, source, confidence)
