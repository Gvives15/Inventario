Campos requeridos (operación mínima)

- REQUIRES_REVIEW
  - review_reason_code: obligatorio
  - review_reason_note: recomendado
- Resolver REVIEW
  - note de resolución: obligatorio
  - transición válida: REQUIRES_REVIEW → PREPARING o CANCELLED
- PAID
  - solo válido si ops_status actual es DELIVERED
- Auditoría
  - OrderOpsEventModel debe registrar cada transición con note y timestamps
 
update_fields críticos (confirmados)
- handle_wa_order_h
  - ["status", "ops_status", "review_reason_code", "review_reason_note", "updated_at"]
- confirm_order_cmd
  - ["ops_status", "updated_at"]
  - ["status", "ops_status", "updated_at"]
- change_ops_status_cmd
  - ["ops_status", "review_reason_code", "review_reason_note", "ops_notes", "ops_updated_at", "updated_at"]
