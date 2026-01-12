# Reason Code: CANCEL_AFTER_CONFIRM

**Código**: `RC_CANCEL_AFTER_CONFIRM`
**Severidad**: Media

## Ficha Técnica

*   **Definición**: El cliente solicita cancelar el pedido después de haber sido confirmado.
*   **Causa Típica**: Arrepentimiento, encontró otro proveedor, demora percibida o emergencia personal.
*   **Qué se pide al cliente**: Motivo de cancelación (para feedback) y confirmación de baja.
    *   *Template*: [`TPL-REV-02`](../06_templates/TPL-REV-02_CANCEL_AFTER_CONFIRM.md)
*   **Resolución Permitida**:
    *   `CANCELLED`: Acción directa tras confirmar la voluntad del cliente.
*   **Deadline Sugerido**: Inmediato.
