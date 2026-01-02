from django.db import IntegrityError
from contact.models import MessageInboundModel


def create_if_new(dto: dict) -> tuple[bool, int | None]:
    try:
        obj = MessageInboundModel.objects.create(
            provider=dto.get("provider", ""),
            provider_message_id=dto.get("provider_message_id", ""),
            whatsapp_id=dto.get("whatsapp_id", ""),
            text=dto.get("text", ""),
            raw_payload=dto.get("raw_payload", ""),
        )
        return True, obj.id
    except IntegrityError:
        return False, None
