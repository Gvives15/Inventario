from contact.models import Contact, ConversationStateModel
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from django.db.models import Q


def get_by_whatsapp_id(whatsapp_id: str) -> Contact | None:
    try:
        return Contact.objects.get(whatsapp_id=whatsapp_id)
    except Contact.DoesNotExist:
        return None


def upsert_minimal(whatsapp_id: str, name: str, zone: str, business_type: str) -> Contact:
    obj = get_by_whatsapp_id(whatsapp_id)
    if obj is None:
        obj = Contact.objects.create(
            whatsapp_id=whatsapp_id,
            name=name,
            business_type=business_type,
            type=Contact.TYPE_CLIENT,
            is_active=True,
        )
    else:
        obj.name = name
        obj.business_type = business_type
        obj.save(update_fields=["name", "business_type", "updated_at"])

    # ensure ConversationState exists at E1_MIN_DATA
    if not ConversationStateModel.objects.filter(contact_id=obj.id).exists():
        ConversationStateModel.objects.create(contact_id=obj.id, stage=ConversationStage.E1_MIN_DATA.value)
    return obj
