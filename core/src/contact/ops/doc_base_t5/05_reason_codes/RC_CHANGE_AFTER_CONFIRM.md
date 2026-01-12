# Reason Code: CHANGE_AFTER_CONFIRM

**Código**: `RC_CHANGE_AFTER_CONFIRM`
**Severidad**: Media

## Ficha Técnica

*   **Definición**: El cliente solicita modificaciones en el pedido después de haber sido confirmado.
*   **Causa Típica**: Olvidó agregar un ítem, quiere cambiar sabor/variedad, o ajustar cantidades.
*   **Qué se pide al cliente**: Confirmación final del nuevo detalle y total del pedido.
    *   *Template*: [`TPL-REV-03`](../06_templates/TPL-REV-03_CHANGE_AFTER_CONFIRM.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Tras editar la orden y re-confirmar con el cliente.
    *   `CANCELLED`: Si el cambio implica cancelar y hacer uno nuevo (aunque preferible editar).
*   **Deadline Sugerido**: +24h.
