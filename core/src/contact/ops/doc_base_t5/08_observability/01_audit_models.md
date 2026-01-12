Modelos de Auditoría

### Referencias de código
- **OrderOpsEvent**: [models.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L116) (Modelo de Evento Ops)
- **MessageEventLog**: [message_event_models.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/messaging/infrastructure/orm/message_event_models.py) (Log de Mensajería)
- **Repo**: [message_event_repo.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/messaging/infrastructure/orm/message_event_repo.py) (Queries de Eventos)

- OrderOpsEventModel
  - Campos: order, from_status, to_status, note, at
  - Uso: timeline de cambios por order_id
- MessageEventLogModel
  - Campos: provider, direction, external_event_id, echo_id, conversation_external_id, status, payload_json
  - Uso: dedupe inbound/outbound; trazabilidad de eventos

