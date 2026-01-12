from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from contact.models import OrderModel, OrderOpsEventModel
from contact.modules.orders.domain.order_status import OrderStatus

ALLOWED_TRANSITIONS = {
    OrderModel.OPS_CONFIRMED: {OrderModel.OPS_PREPARING, OrderModel.OPS_REQUIRES_REVIEW, OrderModel.OPS_CANCELLED},
    OrderModel.OPS_PREPARING: {OrderModel.OPS_READY, OrderModel.OPS_REQUIRES_REVIEW, OrderModel.OPS_CANCELLED},
    OrderModel.OPS_READY: {OrderModel.OPS_OUT_FOR_DELIVERY, OrderModel.OPS_REQUIRES_REVIEW, OrderModel.OPS_CANCELLED},
    OrderModel.OPS_OUT_FOR_DELIVERY: {OrderModel.OPS_DELIVERED, OrderModel.OPS_REQUIRES_REVIEW},
    OrderModel.OPS_DELIVERED: {OrderModel.OPS_PAID},
    OrderModel.OPS_REQUIRES_REVIEW: {OrderModel.OPS_PREPARING, OrderModel.OPS_CANCELLED},
}

TERMINAL_STATES = {OrderModel.OPS_CANCELLED, OrderModel.OPS_REPLACED, OrderModel.OPS_PAID}

def execute(order_id: int, new_ops_status: str, note: str | None = None, review_reason_code: str | None = None, review_reason_note: str | None = None, resolve_review: bool = False) -> OrderModel:
    with transaction.atomic():
        order = OrderModel.objects.select_for_update().get(id=order_id)

        if order.ops_status in TERMINAL_STATES:
            raise ValidationError(f"Estado terminal {order.ops_status}: no se permiten cambios")

        if order.status != OrderStatus.CONFIRMED.value and new_ops_status != OrderModel.OPS_CANCELLED:
            raise ValidationError("Solo se puede operar órdenes CONFIRMED (salvo CANCELLED)")

        current = order.ops_status or OrderModel.OPS_CONFIRMED

        if resolve_review and current != OrderModel.OPS_REQUIRES_REVIEW:
            raise ValidationError("Resolver REVIEW solo desde REQUIRES_REVIEW")

        if resolve_review and not note:
            raise ValidationError("Resolver REVIEW requiere nota")

        if current not in ALLOWED_TRANSITIONS or new_ops_status not in ALLOWED_TRANSITIONS[current]:
            raise ValidationError(f"Transición no permitida: {current} → {new_ops_status}")

        if new_ops_status == OrderModel.OPS_PAID and current != OrderModel.OPS_DELIVERED:
            raise ValidationError("PAID solo es válido después de DELIVERED")

        if new_ops_status == OrderModel.OPS_REQUIRES_REVIEW and not review_reason_code:
            raise ValidationError("REQUIRES_REVIEW exige review_reason_code")

        order.ops_status = new_ops_status
        if new_ops_status == OrderModel.OPS_REQUIRES_REVIEW:
            order.review_reason_code = review_reason_code or OrderModel.REVIEW_MANUAL
            order.review_reason_note = review_reason_note
        if note:
            order.ops_notes = (order.ops_notes or "") + (("\n" if order.ops_notes else "") + note)
        order.save(update_fields=["ops_status", "review_reason_code", "review_reason_note", "ops_notes", "ops_updated_at", "updated_at"])

        OrderOpsEventModel.objects.create(
            order=order,
            from_status=current,
            to_status=new_ops_status,
            note=note,
            review_reason_code=order.review_reason_code,
            review_reason_note=order.review_reason_note,
        )

        return order
