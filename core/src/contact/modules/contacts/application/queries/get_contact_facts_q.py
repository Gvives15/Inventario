from typing import Any
from contact.modules.contacts.infrastructure.orm.contact_history_repo import get_facts_dict


def get_contact_facts_q(contact_id: int) -> dict[str, Any]:
    return get_facts_dict(contact_id)
