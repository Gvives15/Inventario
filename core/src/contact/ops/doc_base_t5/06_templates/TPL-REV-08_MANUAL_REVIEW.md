# Template: MANUAL_REVIEW

**ID**: `TPL-REV-08`
**Reason Code**: `RC_MANUAL_REVIEW`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Consulta genérica no tipificada.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `order_id`
    *   `details` (consulta específica)

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, te escribimos por el pedido #{order_id}.

Necesitamos consultarte algo antes de prepararlo: {details}.

¿Nos confirmás?
```

## Reglas de Uso
*   Usar solo cuando no aplique otro template específico.
*   Redactar `details` de forma clara y cerrada (sí/no) si es posible.
