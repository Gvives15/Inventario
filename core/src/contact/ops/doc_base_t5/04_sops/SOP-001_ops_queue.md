SOP-001 — Cola Operacional (Ops Queue)

- Objetivo
  - Operar la cola de pedidos a través de estados válidos con auditoría.
- Estados involucrados
  - CONFIRMED → PREPARING → READY → OUT_FOR_DELIVERY → DELIVERED → PAID
  - Excepciones: REQUIRES_REVIEW, CANCELLED, REPLACED
- Acciones en Admin
  - to_preparing, to_ready, to_out, to_delivered, to_paid, to_cancelled
  - to_review, to_review_generic
- Guardrails
  - Validaciones de transición (ALLOWED_TRANSITIONS)
  - PAID solo desde DELIVERED
  - REQUIRES_REVIEW exige review_reason_code
- Auditoría
  - Cada transición crea OrderOpsEventModel con from_status, to_status, note.
- DoD
  - Acciones admin ejecutables
  - Transiciones registradas en OrderOpsEventModel
  - Conteo por ops_status verificable
- Checks
  - python manage.py simulate_sop001
  - Consultas: conteo por ops_status; timeline de OrderOpsEvent por order_id

