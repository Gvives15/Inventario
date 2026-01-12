from contact.modules.contacts.infrastructure.orm.contact_external_identity_repo import get_contact_by_identity, create_identity
from contact.modules.conversations.infrastructure.orm import contact_repo
from contact.modules.contacts.infrastructure.orm.contact_history_repo import upsert_fact


def execute(contact_external_id: str, conversation_id: str, inbox_identifier: str | None = None, contact_identifier: str | None = None) -> int:
    provider = "chatwoot"
    c = get_contact_by_identity(provider, contact_external_id)
    if c is None:
        c = contact_repo.upsert_minimal(f"chatwoot:{contact_external_id}", "", "", "")
        create_identity(c, provider, contact_external_id)
    upsert_fact(c.id, "chatwoot_conversation_id", conversation_id, "SYSTEM")
    if inbox_identifier:
        upsert_fact(c.id, "chatwoot_inbox_id", inbox_identifier, "SYSTEM")
    if contact_identifier:
        upsert_fact(c.id, "chatwoot_contact_id", contact_identifier, "SYSTEM")
    return c.id

