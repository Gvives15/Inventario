# Template: CHANGE_AFTER_CONFIRM

**ID**: `TPL-REV-03`
**Reason Code**: `RC_CHANGE_AFTER_CONFIRM`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Cliente solicita cambios en pedido confirmado.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `order_id`

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, perfecto. Vamos a editar tu pedido #{order_id} con los cambios que nos pediste.

En breve te enviamos el nuevo detalle actualizado para que confirmes que está todo OK.
```

## Reglas de Uso
*   Editar el pedido en el sistema.
*   Siempre re-confirmar el total y los ítems con el cliente tras la edición.
