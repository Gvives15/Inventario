# Template: ORDER_REPLACED

**ID**: `TPL-REV-04`
**Reason Code**: `RC_ORDER_REPLACED`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Detección de pedido duplicado o reemplazo.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `old_order_id`
    *   `new_order_id`

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, vemos que ingresó un nuevo pedido (#{new_order_id}).

¿Este reemplaza al anterior (#{old_order_id})?

Si es así, cancelamos el viejo y preparamos el nuevo. ¿Nos confirmás?
```

## Reglas de Uso
*   Solo enviar si hay duda genuina.
*   Si es obvio (mismos ítems + corrección menor), asumir reemplazo y notificar acción tomada.
