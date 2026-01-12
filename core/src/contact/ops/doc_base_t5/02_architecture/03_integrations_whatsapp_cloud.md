Integración WhatsApp Cloud

### Referencias de código
- **Webhook**: [whatsapp_webhook_h.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/application/handlers/whatsapp_webhook_h.py) (Entrypoint + Dedupe)
- **Dedupe In**: [was_event_processed_q.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/messaging/application/queries/was_event_processed_q.py)
- **Log Cmd**: [log_inbound_event_cmd.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/messaging/application/commands/log_inbound_event_cmd.py)
- **Outbound**: [wa_outbound_service.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/application/services/wa_outbound_service.py) (Service + Dedupe Out)

### Rutas y Endpoints
- **Definición**: [routes.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/routes.py)
  - `GET /api/contacts/webhooks/whatsapp_cloud/`: Verificación de webhook.
  - `POST /api/contacts/webhooks/whatsapp_cloud/`: Inbound events.

### Handlers
- **Orders**: [handle_wa_order_h.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/application/handlers/handle_wa_order_h.py)
  - Procesa mensajes tipo "order" (carrito).
  - Lógica: `unknown SKUs` → `REQUIRES_REVIEW`.

### Cliente HTTP
- **Implementación**: [wa_client.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/infrastructure/wa_client.py)
  - Métodos: `send_text`, `send_product_list`.
  - Config: Usa `WHATSAPP_ACCESS_TOKEN`.
- Settings
  - WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_CATALOG_ID
  - WHATSAPP_VERIFY_TOKEN, WHATSAPP_APP_SECRET
- Dedupe
  - Inbound: por external_event_id; duplicados SKIPPED_DUPLICATE.
  - Outbound: por echo_id; servicio outbound genera clave diaria determinística.

