# Queries de Debug y Observabilidad

Queries útiles para diagnosticar el estado de la cola de operaciones.

## 1. Review Queue

### Conteo de órdenes en Review
```python
OrderModel.objects.filter(ops_status="REQUIRES_REVIEW").count()
```
```sql
SELECT COUNT(*) AS total
FROM order_model
WHERE ops_status = 'REQUIRES_REVIEW';
```

### Órdenes Overdue (Vencidas)
```python
from django.utils import timezone
now = timezone.now()
OrderModel.objects.filter(
    ops_status="REQUIRES_REVIEW", 
    review_deadline_at__lt=now
).count()
```
```sql
SELECT COUNT(*) AS total
FROM order_model
WHERE ops_status = 'REQUIRES_REVIEW'
  AND review_deadline_at < NOW();
```

### Órdenes sin Deadline (Deuda Operativa)
```python
OrderModel.objects.filter(
    ops_status="REQUIRES_REVIEW", 
    review_deadline_at__isnull=True
).count()
```
```sql
SELECT COUNT(*) AS total
FROM order_model
WHERE ops_status = 'REQUIRES_REVIEW'
  AND review_deadline_at IS NULL;
```

## 2. Historial y Auditoría

### Timeline de eventos por Orden (ID)
Ver todos los cambios de estado y notas de una orden específica.
```python
OID = 123 # ID de la orden
events = OrderOpsEventModel.objects.filter(order_id=OID).order_by("created_at")
for e in events:
    print(f"{e.created_at} | {e.from_status} -> {e.to_status} | Note: {e.note} | Code: {e.reason_code}")
```
```sql
SELECT created_at, from_status, to_status, note, reason_code
FROM order_ops_event_model
WHERE order_id = 123
ORDER BY created_at ASC;
```

## 3. General

### Conteo por Estado Operativo
```python
from django.db.models import Count
OrderModel.objects.values("ops_status").annotate(total=Count("id")).order_by("ops_status")
```
```sql
SELECT ops_status, COUNT(id) AS total
FROM order_model
GROUP BY ops_status
ORDER BY ops_status;
```

### Últimos logs de WhatsApp por ID
```python
WA_ID = "54911..."
MessageEventLogModel.objects.filter(
    provider="whatsapp_cloud", 
    conversation_external_id=WA_ID
).order_by("-created_at")[:5]
```
```sql
SELECT *
FROM message_event_log_model
WHERE provider = 'whatsapp_cloud'
  AND conversation_external_id = '54911...'
ORDER BY created_at DESC
LIMIT 5;
```
