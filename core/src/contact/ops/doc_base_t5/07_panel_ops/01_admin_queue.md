Panel Ops — Admin

### Referencias de código
- **Admin**: [admin.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/admin.py) (Configuración de Panel)
- **Guardrails**: [test_ops_status_transitions.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/tests/test_ops_status_transitions.py) (Tests de Transiciones)
- **Simulador**: [simulate_sop001.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/management/commands/simulate_sop001.py) (Flujo Diario)

### 1. Order Admin (Operación General)
- **Objetivo**: Visión limpia del flujo diario. Sin ruido de deadlines ni excepciones complejas.
- **Lista y filtros**
  - list_display: id, created_at, contact, zone_name, items_count, ops_status, review_reason_code
  - list_filter: ops_status, created_at, zone (ZoneFilter)
- **Acciones principales**
  - Transiciones rápidas: to_preparing, to_ready, to_out, to_delivered, to_paid, to_cancelled
  - Enviar a revisión: to_review, to_review_generic
  - Asignar zona: assign_zone_to_contact (Bulk)

### 2. Review Queue (Gestión de Excepciones)
- **Objetivo**: Tablero priorizado para resolver problemas.
- **Ubicación**: Menú "Review Queue" (Proxy Model).
- **Lista y filtros**
  - list_display: id, created_at, contact, zone_name, items_count, ops_status, review_reason_code, **review_deadline_at**
  - list_filter: **ReviewQueueFilter** (Pending, Overdue, No deadline), ZoneFilter
  - **Editable**: review_deadline_at (Inline)
- **Acciones exclusivas**
  - Resolver: resolve_review_to_preparing, resolve_review_to_cancelled
  - Gestión de tiempos: set_deadline_24h, set_deadline_72h
- Cómo abrir
  - /admin/ (Django Admin)

