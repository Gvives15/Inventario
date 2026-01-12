from typing import Any
from contact.modules.contacts.infrastructure.orm.contact_history_repo import (
    get_facts_dict,
    get_or_create_reorder_profile,
)


def get_contact_profile_q(contact_id: int) -> dict[str, Any]:
    facts = get_facts_dict(contact_id)
    profile = get_or_create_reorder_profile(contact_id)
    return {
        "facts": facts,
        "reorder_profile": {
            "status": profile.status,
            "cadence_days": profile.cadence_days,
            "preferred_weekdays": profile.preferred_weekdays,
            "next_reorder_date": profile.next_reorder_date,
            "default_list_code": profile.default_list_code,
        },
    }
