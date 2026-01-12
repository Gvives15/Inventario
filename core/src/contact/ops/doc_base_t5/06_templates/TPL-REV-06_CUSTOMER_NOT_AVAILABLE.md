# Template: CUSTOMER_NOT_AVAILABLE

**ID**: `TPL-REV-06`
**Reason Code**: `RC_CUSTOMER_NOT_AVAILABLE`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Cliente no responde intentos de contacto.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `order_id`

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, intentamos contactarte para entregar tu pedido #{order_id} pero no tuvimos suerte.

Por favor avisanos cuando estés disponible para reprogramar.

Si no tenemos noticias en 24hs, tendremos que cancelarlo para liberar el stock. ¡Gracias!
```

## Reglas de Uso
*   Usar tras al menos 1 intento de llamada fallido.
*   Cumplir el plazo de 24h antes de cancelar.
