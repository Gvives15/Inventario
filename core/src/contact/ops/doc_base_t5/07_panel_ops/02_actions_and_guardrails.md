Acciones y Guardrails

- Acciones
  - to_preparing, to_ready, to_out, to_delivered, to_paid, to_cancelled
  - to_review, to_review_generic
  - resolve_review_to_preparing, resolve_review_to_cancelled
- Guardrails (validaciones)
  - ALLOWED_TRANSITIONS determinan movimientos válidos.
  - PAID solo desde DELIVERED.
  - Resolver REVIEW solo desde REQUIRES_REVIEW.
  - REQUIRES_REVIEW exige review_reason_code (nota recomendada).
- Notas
  - Toda acción debe generar OrderOpsEventModel con note cuando corresponda.

