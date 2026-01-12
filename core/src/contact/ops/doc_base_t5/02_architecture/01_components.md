### 1. Órdenes (Core)
- **Modelo**: `OrderModel`
- **Comandos**:
  - `change_ops_status_cmd`: [change_ops_status_cmd.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/orders/application/commands/change_ops_status_cmd.py) - Gestiona transiciones y validaciones.
  - `confirm_order_cmd`: [confirm_order_cmd.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/orders/application/commands/confirm_order_cmd.py) - Confirma orden desde carrito.

### 2. Admin (Panel Ops)
- **Vistas**: Django Admin estándar + acciones personalizadas.
- **Acciones**: "Resolver Review", "Cancelar", etc.

### 3. WhatsApp Cloud (Gateway)
- **Rutas**: Webhooks para inbound/outbound status.
- **Handlers**: [handle_wa_order_h.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/gateways/whatsapp_cloud/application/handlers/handle_wa_order_h.py) - Procesa payloads de órdenes.

### 4. Mensajería (Logs)
- **Modelo**: `MessageEventLogModel`
- **Repo**: Deduplicación por `external_event_id` (in) y `echo_id` (out).

### 5. Settings
- **Variables**: `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, etc.

### 6. Simulación
- **Comando**: `simulate_sop001`: [simulate_sop001.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/management/commands/simulate_sop001.py) - Script de smoke test E2E.
