# Template: CANCEL_AFTER_CONFIRM

**ID**: `TPL-REV-02`
**Reason Code**: `RC_CANCEL_AFTER_CONFIRM`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Cliente solicita cancelar pedido confirmado.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `order_id`

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, recibimos tu solicitud para cancelar el pedido #{order_id}.

Ya procedimos a darlo de baja.

¿Nos podrías contar brevemente el motivo? Nos ayuda mucho a mejorar para la próxima.

¡Saludos!
```

## Reglas de Uso
*   Proceder a la cancelación inmediata en el sistema (Status: CANCELLED).
*   No intentar "recuperar" la venta agresivamente. Aceptar la decisión.
