# Doc Base T5 — Índice Navegable

**Qué es**
- Documentación modular del “Sistema de Pedidos Eficiente (T5)”.
- Contiene SOPs activos, códigos de referencia y guías de operación.

**Cómo navegar**
- Entrá por secciones; cada archivo trata un único tema.
- Los links son relativos; se puede explorar sin buscador global.

## Secciones

### North Star
- [01_objective.md](./01_north_star/01_objective.md)
- [02_principles.md](./01_north_star/02_principles.md)
- [03_glossary.md](./01_north_star/03_glossary.md)

### Arquitectura
- [01_components.md](./02_architecture/01_components.md)
- [02_end_to_end_flows.md](./02_architecture/02_end_to_end_flows.md)
- [03_integrations_whatsapp_cloud.md](./02_architecture/03_integrations_whatsapp_cloud.md)

### Data Contract
- [01_entities.md](./03_data_contract/01_entities.md)
- [02_fields_required.md](./03_data_contract/02_fields_required.md)
- [03_state_machines.md](./03_data_contract/03_state_machines.md)

### SOPs
- [SOP-001_ops_queue.md](./04_sops/SOP-001_ops_queue.md)
- [SOP-002_requires_review.md](./04_sops/SOP-002_requires_review.md) (Gestión de Excepciones)
- [SOP_TEMPLATE.md](./04_sops/SOP_TEMPLATE.md)

### Reason Codes (Review)
- [00_reason_codes_index.md](./05_reason_codes/00_reason_codes_index.md)
- [RC_SKU_UNKNOWN.md](./05_reason_codes/RC_SKU_UNKNOWN.md)
- [RC_CANCEL_AFTER_CONFIRM.md](./05_reason_codes/RC_CANCEL_AFTER_CONFIRM.md)
- [RC_CHANGE_AFTER_CONFIRM.md](./05_reason_codes/RC_CHANGE_AFTER_CONFIRM.md)
- [RC_ORDER_REPLACED.md](./05_reason_codes/RC_ORDER_REPLACED.md)
- [RC_ADDRESS_OUT_OF_ZONE.md](./05_reason_codes/RC_ADDRESS_OUT_OF_ZONE.md)
- [RC_CUSTOMER_NOT_AVAILABLE.md](./05_reason_codes/RC_CUSTOMER_NOT_AVAILABLE.md)
- [RC_PAYMENT_ISSUE.md](./05_reason_codes/RC_PAYMENT_ISSUE.md)
- [RC_MANUAL_REVIEW.md](./05_reason_codes/RC_MANUAL_REVIEW.md)

### Templates (WhatsApp)
- [00_templates_index.md](./06_templates/00_templates_index.md)
- [TPL-REV-01_SKU_UNKNOWN.md](./06_templates/TPL-REV-01_SKU_UNKNOWN.md)
- [TPL-REV-02_CANCEL_AFTER_CONFIRM.md](./06_templates/TPL-REV-02_CANCEL_AFTER_CONFIRM.md)
- [TPL-REV-03_CHANGE_AFTER_CONFIRM.md](./06_templates/TPL-REV-03_CHANGE_AFTER_CONFIRM.md)
- [TPL-REV-04_ORDER_REPLACED.md](./06_templates/TPL-REV-04_ORDER_REPLACED.md)
- [TPL-REV-05_ADDRESS_OUT_OF_ZONE.md](./06_templates/TPL-REV-05_ADDRESS_OUT_OF_ZONE.md)
- [TPL-REV-06_CUSTOMER_NOT_AVAILABLE.md](./06_templates/TPL-REV-06_CUSTOMER_NOT_AVAILABLE.md)
- [TPL-REV-07_PAYMENT_ISSUE.md](./06_templates/TPL-REV-07_PAYMENT_ISSUE.md)
- [TPL-REV-08_MANUAL_REVIEW.md](./06_templates/TPL-REV-08_MANUAL_REVIEW.md)

### Panel Ops (Admin)
- [01_admin_queue.md](./07_panel_ops/01_admin_queue.md)
- [02_actions_and_guardrails.md](./07_panel_ops/02_actions_and_guardrails.md)
- [03_failure_modes.md](./07_panel_ops/03_failure_modes.md)

### Observabilidad
- [01_audit_models.md](./08_observability/01_audit_models.md)
- [02_queries_debug.md](./08_observability/02_queries_debug.md)
- [03_smoke_tests.md](./08_observability/03_smoke_tests.md)

### DoD & Checks
- [01_dod_t5.md](./09_dod_checks/01_dod_t5.md)
- [02_checks_runbook.md](./09_dod_checks/02_checks_runbook.md)

### Backlog
- [01_now_next_later.md](./10_backlog/01_now_next_later.md)
