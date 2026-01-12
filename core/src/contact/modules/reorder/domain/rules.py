from contact.models import OrderModel


def has_active_proposed(contact_id: int) -> bool:
    return OrderModel.objects.filter(contact_id=contact_id, status="PROPOSED").exists()

