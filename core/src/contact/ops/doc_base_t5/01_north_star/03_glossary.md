Glosario

- OrderModel: entidad de pedido; campos clave status y ops_status.
- ops_status: estado operacional; choices reales CONFIRMED, REQUIRES_REVIEW, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, PAID, CANCELLED, REPLACED.
- review_reason_code: motivo de revisión; choices reales SKU_UNKNOWN, CHANGE_AFTER_CONFIRM, CANCEL_AFTER_CONFIRM, ORDER_REPLACED, ADDRESS_OUT_OF_ZONE, CUSTOMER_NOT_AVAILABLE, PAYMENT_ISSUE, MANUAL_REVIEW.
- review_reason_note: nota libre asociada al motivo de revisión.
- OrderOpsEventModel: registro de transición operacional (from_status, to_status, note, timestamps).
- MessageEventLogModel: logs de eventos de mensajería (provider, direction, external_event_id, echo_id, conversation_external_id, status, payload_json).
- WhatsApp Cloud: gateway de mensajería entrante/saliente con deduplicación y firma.

