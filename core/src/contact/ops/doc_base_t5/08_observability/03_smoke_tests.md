Smoke Tests (mínimos)

- Simulación de flujo básico
  - python manage.py simulate_sop001
- Tests de resolución REVIEW
  - python manage.py test contact.tests.test_sop002_review_resolution
- Idempotencia inbound/outbound
  - python manage.py test contact.tests.test_event_log_idempotency_inbound
  - python manage.py test contact.tests.test_event_log_idempotency_outbound

