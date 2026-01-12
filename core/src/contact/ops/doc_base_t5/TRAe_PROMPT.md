Tenés acceso al repo local. Objetivo: completar y validar el Doc Base modular de T5.

REGLA 1: No inventes nada. Todo debe salir del repo (código, tests, settings, comandos).
REGLA 2: Si algo no existe, dejalo como TBD y explicitá qué falta.
REGLA 3: Si encontrás discrepancias, corregí el doc y escribí “Correcciones aplicadas” al inicio del index.

RUTA A COMPLETAR:
core/src/contact/ops/doc_base_t5/

TAREAS:
A) Reemplazar TBD con datos reales del repo:
- nombres exactos de modelos: OrderModel, OrderOpsEventModel, MessageEventLogModel (o equivalentes)
- enums exactos ops_status y review_reason_code (OrderModel.OPs_STATUS_CHOICES, REVIEW_CODE_CHOICES)
- paths exactos de comandos (confirm_order_cmd.py, change_ops_status_cmd.py, management/commands/simulate_sop001.py)
- rutas/handlers WA Cloud (routes.py, handlers, mapping)
- settings y variables WA (WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_CATALOG_ID, WHATSAPP_VERIFY_TOKEN, WHATSAPP_APP_SECRET, WA_GRAPH_BASE_URL, WA_API_VERSION)

B) Completar links y comandos reales:
- comandos para migrate, test, simulate_sop001
- cómo abrir admin (/admin/)
- queries reales (ORM/SQL) para:
  - conteo por ops_status
  - timeline OrderOpsEventModel por order_id
  - últimos MessageEventLogModel por wa_id

C) Validar SOP-001 contra el sistema real:
- acciones admin existentes
- guardrails reales de transición (ALLOWED_TRANSITIONS, TERMINAL_STATES)
- auditoría real (qué campos quedan)

D) SOP-002:
- Si está implementado, documentar cómo se ejecuta en el panel
- Si no está implementado, dejar backlog mínimo con qué faltaría (acción “resolver review”, nota obligatoria, tests)

E) Output:
- actualizar todos los archivos del doc_base_t5
- actualizar 00_index.md
- agregar sección “Correcciones aplicadas” arriba del 00_index.md con lista bullet de cambios.

