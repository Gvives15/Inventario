from contact.shared.infrastructure.uow import UnitOfWork


def execute(whatsapp_id: str, name: str | None = None, zone: str | None = None, business_type: str | None = None) -> int:
    with UnitOfWork() as uow:
        c = uow.contacts.get_by_whatsapp_id(whatsapp_id)
        if c is None:
            c = uow.contacts.upsert_minimal(whatsapp_id, name or "", zone or "", business_type or "")
        else:
            c = uow.contacts.upsert_minimal(whatsapp_id, name or c.name, zone or c.zone, business_type or c.business_type)
        return c.id
