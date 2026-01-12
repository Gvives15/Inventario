from typing import Optional
from contact.models import Contact
from contact.modules.contacts.infrastructure.orm.contact_external_identity_models import ContactExternalIdentityModel


def get_contact_by_identity(provider: str, external_id: str) -> Optional[Contact]:
    try:
        obj = ContactExternalIdentityModel.objects.get(provider=provider, external_id=external_id)
        return obj.contact
    except ContactExternalIdentityModel.DoesNotExist:
        return None


def create_identity(contact: Contact, provider: str, external_id: str) -> ContactExternalIdentityModel:
    obj, _ = ContactExternalIdentityModel.objects.update_or_create(
        provider=provider,
        external_id=external_id,
        defaults={"contact": contact},
    )
    return obj

