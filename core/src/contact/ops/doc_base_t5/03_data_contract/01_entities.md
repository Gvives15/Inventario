Entidades (conceptual y mapeo real)

### 1. OrderModel
**Ubicación**: [models.py:L28](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L28)

Modelo central que agrupa la información del pedido.

- **`ops_status`**: [models.py:L51](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L51) - Estado operativo (CONFIRMED, PREPARING, etc.).
- **`review_reason_code`**: [models.py:L70](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L70) - Razón de revisión si requiere atención.
- **`review_deadline_at`**: Fecha límite para resolución de revisión.
- **`contact`**: Relación con el cliente.

### 2. ZoneModel
**Ubicación**: [models.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py)

Zonificación para logística y asignación de pedidos.

- **`name`**: Nombre de la zona (ej: "CPC - Norte").
- **`code`**: Código único.
- **`is_active`**: Soft delete.

### 3. OrderReviewQueue (Proxy)
**Ubicación**: [models.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py)

Proyección de `OrderModel` filtrada para el flujo de revisión.

### 4. OrderOpsEventModel
**Ubicación**: [models.py:L116](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L116)

Registro de auditoría de cambios de estado operativo.

### 5. MessageEventLogModel
**Ubicación**: [message_event_models.py:L6](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/messaging/infrastructure/orm/message_event_models.py#L6)

