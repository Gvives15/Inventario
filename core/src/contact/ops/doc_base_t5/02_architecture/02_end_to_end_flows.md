Flujos End-to-End (alto nivel)

### Referencias de código
- **Confirmación**: [confirm_order_cmd.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/orders/application/commands/confirm_order_cmd.py) (Transición a CONFIRMED + Evento Ops)
- **Handler WA**: [handle_wa_order_h.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/application/handlers/handle_wa_order_h.py) (Entrada por WA + Review Logic)

- Happy Path
  - CONFIRMED → PREPARING → READY → OUT_FOR_DELIVERY → DELIVERED → PAID
- Excepciones
  - REQUIRES_REVIEW (entra por handler WA o acción admin)
  - CANCELLED (terminal)
  - REPLACED (terminal)
- Guardrails (validaciones clave)
  - PAID solo válido después de DELIVERED.
  - Resolver REVIEW solo desde REQUIRES_REVIEW.
  - REQUIRES_REVIEW exige review_reason_code (y nota opcional).
- Auditoría
  - Cada transición crea OrderOpsEventModel con from_status, to_status, note.

