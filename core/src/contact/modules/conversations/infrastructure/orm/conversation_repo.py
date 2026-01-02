from contact.models import ConversationStateModel, Contact, OrderModel
from contact.modules.conversations.domain.conversation_stage import ConversationStage


def get_by_contact_id(contact_id: int) -> ConversationStateModel | None:
    try:
        return ConversationStateModel.objects.get(contact_id=contact_id)
    except ConversationStateModel.DoesNotExist:
        return None


def set_stage_and_last_order(contact_id: int, stage: ConversationStage, last_order_id: int | None) -> ConversationStateModel:
    obj = get_by_contact_id(contact_id)
    if stage == ConversationStage.E2_PROPOSAL and not last_order_id:
        raise ValueError("last_order required for E2_PROPOSAL")
    last_order = None
    if last_order_id:
        try:
            last_order = OrderModel.objects.get(id=last_order_id)
        except OrderModel.DoesNotExist:
            raise ValueError("last_order not found")
    if obj is None:
        return ConversationStateModel.objects.create(contact_id=contact_id, stage=stage.value, last_order=last_order)
    obj.stage = stage.value
    obj.last_order = last_order
    obj.save(update_fields=["stage", "last_order", "updated_at"])
    return obj
