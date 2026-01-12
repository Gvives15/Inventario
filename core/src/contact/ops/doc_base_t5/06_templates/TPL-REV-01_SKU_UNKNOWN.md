# Template: SKU_UNKNOWN

**ID**: `TPL-REV-01`
**Reason Code**: `RC_SKU_UNKNOWN`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Pedido marcado con `SKU_UNKNOWN` por el sistema.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `unknown_skus` (lista de productos no reconocidos)
    *   `order_id`

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, estamos revisando tu pedido #{order_id} pero tenemos una duda.

El sistema no reconoció estos productos: {unknown_skus}.

¿Podrías confirmarnos qué querías pedir exactamente? Así lo corregimos y avanzamos con la preparación.

¡Gracias!
```

## Reglas de Uso
*   No adivinar el producto. Esperar confirmación del cliente.
*   Si el producto no existe, ofrecer similar o remover.
