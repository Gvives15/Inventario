from contact.modules.contacts.infrastructure.orm.contact_history_repo import get_facts_dict


REQUIRED_KEYS = {"name", "business_type"}


def _normalize(s: str) -> str:
    return s.strip()


def _is_valid_required_value(v: object) -> bool:
    if not isinstance(v, str):
        return False
    vv = _normalize(v)
    if len(vv) < 2:
        return False
    if vv in {"-", ".", "m"}:
        return False
    return True


def has_min_profile_q(contact_id: int) -> bool:
    facts = get_facts_dict(contact_id)
    for k in REQUIRED_KEYS:
        if k not in facts:
            return False
        if not _is_valid_required_value(facts[k]):
            return False
    return True
