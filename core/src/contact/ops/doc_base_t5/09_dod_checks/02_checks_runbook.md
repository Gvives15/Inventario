Runbook — Implementation Check

- Migraciones
  - python manage.py migrate
- Tests
  - python manage.py test contact
  - python manage.py test contact.tests.test_sop002_review_resolution
  - python manage.py test contact.tests.test_whatsapp_cloud_eventlog_dedupe_and_mapping
- SOP-002 Smoke Test
  - python manage.py simulate_review_cases
  - Ir al Admin → filtrar ops_status=REQUIRES_REVIEW
  - Seleccionar 1 caso → resolver a PREPARING con nota
  - Verificar que creó OrderOpsEvent con note y que review_reason_code quedó consistente
- Simulación SOP-001
  - python manage.py simulate_sop001
- Admin
  - Abrir /admin/ y verificar filtros por ops_status; acciones disponibles.
- Auditoría
  - Timeline en OrderOpsEventModel por order_id
- EventLog
  - Verificar dedupe inbound/outbound y estados (SKIPPED_DUPLICATE)

