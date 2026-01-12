# Template: PAYMENT_ISSUE

**ID**: `TPL-REV-07`
**Reason Code**: `RC_PAYMENT_ISSUE`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Problema con la validación del pago.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `order_id`
    *   `issue_details` (ej: "no llegó la transferencia", "comprobante ilegible")

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, estamos validando el pago de tu pedido #{order_id}.

Tenemos un inconveniente: {issue_details}.

¿Podrías revisar y enviarnos el comprobante nuevamente?

Gracias.
```

## Reglas de Uso
*   Ser específico con el problema para evitar idas y vueltas.
*   Mantener tono administrativo pero amable.
